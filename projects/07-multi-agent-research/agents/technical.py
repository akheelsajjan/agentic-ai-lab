from llm.model import llm


def technical_agent(query: str) -> str:
    response = llm.invoke(
        f"""
Analyze the following question from a technical perspective.

Focus on:
- Architecture
- Scalability
- Technical tradeoffs

Question:
{query}
"""
    )

    return response.content