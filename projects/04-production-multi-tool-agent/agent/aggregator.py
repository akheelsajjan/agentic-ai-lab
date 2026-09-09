from langchain_groq import ChatGroq


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


def aggregate_results(query: str, results: dict) -> str:
    context = "\n\n".join(
        f"{tool}: {result}"
        for tool, result in results.items()
    )

    prompt = f"""
Answer the user's question using the tool results below.

User question:
{query}

Tool results:
{context}

Rules:
- Use all successful tool results.
- Do not ignore a successful tool result because another tool failed.
- Clearly mention failed tools.
- Do not invent information.
- Give one clear, concise answer.
"""

    response = llm.invoke(prompt)

    return response.content