import json
import asyncio
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv()

# -----------------------
# 1️⃣ LLM
# -----------------------
llm = ChatOpenAI(model="gpt-4o-mini")

# -----------------------
# 2️⃣ MCP CLIENT
# -----------------------
servers = {
    "pdf_reader": {
        "transport": "stdio",
        "command": r"C:\Users\user\Desktop\pdf_mcp_server\.venv\Scripts\fastmcp.exe",
        "args": [
            "run",
            r"C:\Users\user\Desktop\pdf_mcp_server\main.py",
            "--no-banner",
        ],
    }
}

client = MultiServerMCPClient(servers)


# -----------------------
# 3️⃣ STATE
# -----------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# -----------------------
# 4️⃣ CHAT NODE (ASYNC)
# -----------------------
async def chat_node(state: ChatState):
    tools = await client.get_tools()
    llm_with_tools = llm.bind_tools(tools)

    system_message = SystemMessage(
        content="You are a helpful assistant. Use tools when necessary."
    )

    messages = [system_message, *state["messages"]]

    response = await llm_with_tools.ainvoke(messages)

    return {"messages": [response]}


# -----------------------
# 5️⃣ TOOL NODE (MCP tools)
# -----------------------
async def create_tool_node():
    tools = await client.get_tools()
    return ToolNode(tools)


# -----------------------
# 6️⃣ BUILD GRAPH
# -----------------------
async def build_graph():

    tools = await client.get_tools()
    tool_node = ToolNode(tools)

    graph = StateGraph(ChatState)

    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools", "chat_node")

    return graph.compile()


# -----------------------
# 7️⃣ RUN
# -----------------------
from langchain_core.messages import AIMessage

_graph = None

async def get_graph():
    global _graph
    if _graph is None:
        _graph = await build_graph()
    return _graph


async def run_model(messages: list):

    graph = await get_graph()

    # Convert FastAPI dict messages → LangChain messages
    lc_messages = []

    for msg in messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            lc_messages.append(AIMessage(content=msg["content"]))

    result = await graph.ainvoke({
        "messages": lc_messages
    })

    return result["messages"][-1].content