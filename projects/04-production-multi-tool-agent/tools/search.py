import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()


client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def search(query: str) -> str:
    """Search the web for information."""

    response = client.search(
        query=query,
        max_results=3,
    )

    results = []

    for result in response["results"]:
        results.append(
            f"Title: {result['title']}\n"
            f"Content: {result['content']}\n"
            f"URL: {result['url']}"
        )

    return "\n\n".join(results)