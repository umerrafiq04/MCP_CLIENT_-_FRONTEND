# tavily tool
# logic/simple_tools.py

from langchain.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def tavily_search(query: str) -> str:
    """
    Search the web using Tavily and return summarized results.
    """
    response = tavily_client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    # Extract useful content
    results = response.get("results", [])

    formatted = []
    for r in results:
        formatted.append(
            f"Title: {r['title']}\n"
            f"Content: {r['content']}\n"
            f"URL: {r['url']}\n"
        )

    return "\n\n".join(formatted)

def get_simple_tools():
    """
    Parent function that returns all simple tools.
    """
    return [tavily_search]
