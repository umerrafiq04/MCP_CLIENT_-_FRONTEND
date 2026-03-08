from typing import TypedDict, Annotated
import os
from dotenv import load_dotenv

from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    AIMessage,
    ToolMessage,
)

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

from langchain_mistralai import ChatMistralAI
from langchain_mcp_adapters.client import MultiServerMCPClient

from logic.simple_tools import get_simple_tools

load_dotenv()

# -----------------------
# LLM
# -----------------------

from langchain_mistralai import ChatMistralAI

llm = ChatMistralAI(
    model="mistral-large-latest"
)

# -----------------------
# MCP CLIENT
# -----------------------

servers = {
    "expense_tracker": {
        "transport": "stdio",
        "command": r"C:\Users\malik\Desktop\frontend2\.venv\Scripts\fastmcp.exe",
        "args": [
            "run",
            r"C:\Users\malik\Desktop\server\main.py:server",
            "--no-banner",
        ],
    }
}

client = MultiServerMCPClient(servers)

# -----------------------
# STATE
# -----------------------

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    approval: str


# -----------------------
# BUILD GRAPH
# -----------------------

async def build_graph():

    mcp_tools = await client.get_tools()
    simple_tools = get_simple_tools()

    all_tools = mcp_tools + simple_tools

    llm_with_tools = llm.bind_tools(all_tools)

    tool_node = ToolNode(all_tools)

    graph = StateGraph(ChatState)

    DANGEROUS_TOOLS = ["delete_file", "delete_pdf", "create_pdf"]

    # -----------------------
    # CHAT NODE
    # -----------------------

    async def chat_node(state: ChatState):

        system_message = SystemMessage(
            content="""
You are an intelligent assistant that can use external tools to solve user requests.

Your knowledge cutoff is June 8, 2024.

GENERAL BEHAVIOR
- Prefer using available tools whenever they help answer a question more accurately.
- If information might be outdated, real-time, or beyond your knowledge cutoff, use the Tavily search tool.

TOOL USAGE
- Always consider whether a tool can help before answering directly.
- When a task requires multiple steps, plan the steps and use multiple tools if necessary.
- Use tool outputs as the source of truth and base your responses strictly on them.
- Do not fabricate tool results.

FILE AND DOCUMENT TASKS
- When a request involves files or documents, first discover available files using file-listing tools if needed.
- If the user refers to files without specifying exact names, identify potentially relevant files using available tools.
- When necessary, read or analyze files using the appropriate tools to determine their relevance.
- Combine information from multiple files if required.

PARAMETER HANDLING
- If required tool parameters are missing, infer reasonable values from the user request whenever possible.
- If the user request implies searching or filtering content, use the appropriate sequence of tools to accomplish it.

PROBLEM SOLVING
- Break complex tasks into logical steps and execute them using tools when appropriate.
- Prefer exploration and discovery through tools rather than guessing.

COMMUNICATION
- Be concise and clear.
- Focus on completing the user’s request efficiently.
"""
        )

        messages = state["messages"]

        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [system_message] + messages

        # Clean tool messages for Mistral
        cleaned = []

        for m in messages:

            if isinstance(m, ToolMessage) and isinstance(m.content, list):

                text = ""

                for part in m.content:
                    if isinstance(part, dict) and "text" in part:
                        text += part["text"]

                m.content = text

            cleaned.append(m)

        response = await llm_with_tools.ainvoke(cleaned)

        return {"messages": [response]}

    # -----------------------
    # TOOL ROUTER
    # -----------------------

    async def tool_router(state: ChatState):

        last = state["messages"][-1]

        if not hasattr(last, "tool_calls") or not last.tool_calls:
            return END

        tool_name = last.tool_calls[0]["name"]

        if tool_name in DANGEROUS_TOOLS:
            return "human_approval"

        return "tools"

    # -----------------------
    # HUMAN APPROVAL
    # -----------------------

    async def human_approval(state: ChatState):

        last = state["messages"][-1]
        tool_call = last.tool_calls[0]

        tool_name = tool_call["name"]
        args = tool_call["args"]

        messages_map = {
            "delete_file": lambda a: f"⚠️ Delete file '{a.get('path','')}'?",
            "delete_pdf": lambda a: f"⚠️ Delete PDF '{a.get('path','')}'?",
            "create_pdf": lambda a: f"📄 Create PDF '{a.get('filename','')}'?",
        }

        message_fn = messages_map.get(
            tool_name,
            lambda a: f"⚠️ Execute '{tool_name}' with arguments {a}?"
        )

        decision = interrupt(
            f"{message_fn(args)}\n\nType YES to approve or NO to cancel."
        )

        return {"approval": decision}

    # -----------------------
    # APPROVAL ROUTER
    # -----------------------

    async def approval_router(state: ChatState):

        decision = (state.get("approval") or "").strip().lower()

        if decision in ["yes", "y"]:
            return "tools"

        return "cancel"

    # -----------------------
    # CANCEL NODE
    # -----------------------

    async def cancel_node(state: ChatState):

        last = state["messages"][-1]

        if hasattr(last, "tool_calls") and last.tool_calls:

            tool_call = last.tool_calls[0]

            return {
                "messages": [
                    ToolMessage(
                        content="Action cancelled by user.",
                        tool_call_id=tool_call["id"]
                    ),
                    AIMessage(content="❌ Action cancelled.")
                ]
            }

        return {"messages": [AIMessage(content="❌ Action cancelled.")]}

    # -----------------------
    # NODES
    # -----------------------

    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)
    graph.add_node("human_approval", human_approval)
    graph.add_node("cancel", cancel_node)

    # -----------------------
    # EDGES
    # -----------------------

    graph.add_edge(START, "chat_node")

    graph.add_conditional_edges(
        "chat_node",
        tool_router,
        {
            "tools": "tools",
            "human_approval": "human_approval",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "human_approval",
        approval_router,
        {
            "tools": "tools",
            "cancel": "cancel",
        },
    )

    graph.add_edge("tools", "chat_node")
    graph.add_edge("cancel", END)

    checkpointer = MemorySaver()

    return graph.compile(checkpointer=checkpointer)


_graph = None


async def get_graph():

    global _graph

    if _graph is None:
        _graph = await build_graph()

    return _graph


# -----------------------
# STREAMING WITH INTERRUPT SUPPORT
# -----------------------
async def stream_model(messages: list):

    graph = await get_graph()

    lc_messages = []

    for msg in messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            lc_messages.append(AIMessage(content=msg["content"]))

    last_output = ""

    async for event in graph.astream(
        {"messages": lc_messages},
        stream_mode="updates"
    ):

        # -----------------------
        # HANDLE INTERRUPT
        # -----------------------
        if event["type"] == "interrupt":

            approval_text = event["value"]

            # Send approval message to Streamlit
            yield approval_text

            # Wait for frontend to send user approval
            user_input = yield "__WAITING_FOR_APPROVAL__"

            # Resume graph
            async for resumed in graph.astream(
                Command(resume=user_input),
                stream_mode="updates"
            ):
                if resumed["type"] == "messages":
                    message = resumed["value"][-1]
                    if message.type == "ai":
                        yield message.content

            return

        # -----------------------
        # HANDLE NORMAL MESSAGES
        # -----------------------
        if event["type"] == "messages":
            message = event["value"][-1]

            if message.type != "ai":
                continue

            content = message.content or ""

            if content.startswith(last_output):
                delta = content[len(last_output):]
            else:
                delta = content
                last_output = ""

            if delta:
                last_output = content
                yield delta





# ############# previous code without hitl*************

# from logic.simple_tools import get_simple_tools
# import json
# import asyncio
# from typing import TypedDict, Annotated

# from dotenv import load_dotenv
# from langchain_core.messages import BaseMessage, SystemMessage
# from langgraph.graph import StateGraph, START
# from langgraph.graph.message import add_messages
# from langgraph.prebuilt import ToolNode, tools_condition
# from langchain_openai import ChatOpenAI
# from langchain_mcp_adapters.client import MultiServerMCPClient

# load_dotenv()

# # -----------------------
# # LLM
# # -----------------------
# # llm = ChatOpenAI(model="gpt-4o-mini")
# # 
# from langchain_mistralai import ChatMistralAI

# llm = ChatMistralAI(
#     model="mistral-large-latest",
#     mistral_api_key="UrCYglGgzvCqzSSEEaewBCkM9QUITI9p" 
# )
# # -----------------------
# # MCP CLIENT
# # -----------------------
# servers = {
#     "expense_tracker": {
#         "transport": "stdio",
#         "command": r"C:\Users\malik\Desktop\frontend2\.venv\Scripts\fastmcp.exe",
#         "args": [
#             "run",
#             r"C:\Users\malik\Desktop\server\main.py:server",
#             "--no-banner",
#         ],
#     }
# }

# client = MultiServerMCPClient(servers)


# # -----------------------
# # STATE
# # -----------------------
# class ChatState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]


# # -----------------------
# # BUILD GRAPH
# # -----------------------
# async def build_graph():

#     # Fetch MCP tools once
#     mcp_tools = await client.get_tools()

#     #  Merge with simple tools
#     simple_tools = get_simple_tools()
#     all_tools = mcp_tools + simple_tools

#     #  Bind once
#     llm_with_tools = llm.bind_tools(all_tools)

#     # Pass merged tools to ToolNode
#     tool_node = ToolNode(all_tools)

#     graph = StateGraph(ChatState)

#     # -----------------------
#     # CHAT NODE (FIXED)
#     # -----------------------
#     async def chat_node(state: ChatState):

#         system_message = SystemMessage(
#                 content="""
#             You are a tool-executing assistant.

#             Your knowledge cutoff is June 8, 2024.

#             If the user asks about:
#             - current date or time
#             - recent events or news
#             - information after June 8, 2024
#             - real-time data (weather, updates, trends, latest releases)
#             - anything you are unsure about

#             You MUST use the Tavily search tool to retrieve up-to-date information.

#             Rules:
#             - Do NOT guess or hallucinate unknown information.
#             - If the answer may have changed after your knowledge cutoff, use the Tavily tool.
#             - Prefer using tools when fresh or external information is needed.

#             Response behavior:
#             - Do not repeat the user's request.
#             - Do not explain reasoning.
#             - Only return the tool result when a tool is used.
#             - Be concise.
#             """
#             )

#         messages = [system_message, *state["messages"]]

#         # ✅ Ensure all message content is a plain string (required for Mistral)
#         for m in messages:
#             if isinstance(m.content, list):
#                 m.content = "".join(
#                     part["text"] if isinstance(part, dict) and "text" in part else str(part)
#                     for part in m.content
#                 )

#         # NO tool fetching here
#         # NO rebinding here
#         response = await llm_with_tools.ainvoke(messages)

#         return {"messages": [response]}

#     # Add nodes
#     graph.add_node("chat_node", chat_node)
#     graph.add_node("tools", tool_node)

#     # Add edges
#     graph.add_edge(START, "chat_node")
#     graph.add_conditional_edges("chat_node", tools_condition)
#     graph.add_edge("tools", "chat_node")

#     return graph.compile()
# # -----------------------
# # RUN
# # -----------------------
# from langchain_core.messages import AIMessage

# _graph = None

# async def get_graph():
#     global _graph
#     if _graph is None:
#         _graph = await build_graph()
#     return _graph


# # async def run_model(messages: list):

# #     graph = await get_graph()

# #     # Convert FastAPI dict messages → LangChain messages
# #     lc_messages = []

# #     for msg in messages:
# #         if msg["role"] == "user":
# #             lc_messages.append(HumanMessage(content=msg["content"]))
# #         elif msg["role"] == "assistant":
# #             lc_messages.append(AIMessage(content=msg["content"]))

# #     result = await graph.ainvoke({
# #         "messages": lc_messages
# #     })

# #     return result["messages"][-1].content

# # streaming ...
# from langchain_core.messages import HumanMessage, AIMessage

# async def stream_model(messages: list):
#     graph = await get_graph()

#     lc_messages = []

#     for msg in messages:
#         if msg["role"] == "user":
#             lc_messages.append(HumanMessage(content=msg["content"]))
#         elif msg["role"] == "assistant":
#             lc_messages.append(AIMessage(content=msg["content"]))

#     last_output = ""

#     async for state in graph.astream(
#         {"messages": lc_messages},
#         stream_mode="values"
#     ):
#         if "messages" not in state:
#             continue

#         last_message = state["messages"][-1]

#         if last_message.type != "ai":
#             continue

#         content = last_message.content or ""

#         if isinstance(content, list):
#             text = ""
#             for part in content:
#                 if isinstance(part, dict) and part.get("type") == "text":
#                     text += part.get("text", "")
#             content = text

#         # Only stream new part
#         if content.startswith(last_output):
#             delta = content[len(last_output):]
#         else:
#             # If rewritten, reset safely
#             delta = content
#             last_output = ""

#         if delta:
#             last_output = content
#             yield delta

