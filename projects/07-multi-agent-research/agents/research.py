from llm.model import llm
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()


client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

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




def research_agent(query: str) -> str:
    search_results = search(query)

    response = llm.invoke(
        f"""
        You are a research agent.

        Answer the user's question using the search results below.

        Question:
        {query}

        Search results:
        {search_results}

        Focus on factual information.
        Do not invent information.

        At the end, include the URLs of the sources you used.
        """
    )

    return response.content