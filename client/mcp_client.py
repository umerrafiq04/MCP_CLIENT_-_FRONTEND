import json
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI

load_dotenv()

# Initialize once
llm = ChatOpenAI(model="gpt-4o-mini")

servers = {
    "expense": {
        "transport": "stdio",
        "command": r"C:\Users\user\Desktop\CLIENTS\.venv\Scripts\fastmcp.exe",
        "args": [
            "run",
            r"C:\Users\user\Desktop\Servers\main.py",
            "--no-banner",
        ],
    }
}

client = MultiServerMCPClient(servers)


async def run_model(messages):
    tools = await client.get_tools()
    named_tools = {tool.name: tool for tool in tools}

    llm_with_tools = llm.bind_tools(tools)

    # Pass full conversation
    response = await llm_with_tools.ainvoke(messages)

    if not getattr(response, "tool_calls", None):
        return response.content

    tool_messages = []

    for tc in response.tool_calls:
        tool_name = tc["name"]
        tool_args = tc.get("args") or {}
        tool_call_id = tc["id"]

        tool_result = await named_tools[tool_name].ainvoke(tool_args)

        tool_messages.append(
            ToolMessage(
                content=json.dumps(tool_result),
                tool_call_id=tool_call_id
            )
        )

    final_response = await llm_with_tools.ainvoke(
        messages + [response] + tool_messages
    )

    return final_response.content

