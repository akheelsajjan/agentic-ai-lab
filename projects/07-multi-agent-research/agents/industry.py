from llm.model import llm


def industry_agent(query: str) -> str:
    response = llm.invoke(
        f"""
Analyze the following question from an enterprise industry perspective.

Focus on:
- Business considerations
- Operational considerations
- Enterprise use cases

Question:
{query}
"""
    )

    return response.content