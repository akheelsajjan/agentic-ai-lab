from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    return str(eval(expression))


@tool
def search_knowledge(topic: str) -> str:
    """Return information about a topic from a small knowledge base."""

    knowledge = {
        "python": "Python is a high-level programming language.",
        "rag": "RAG combines retrieval with LLM generation to provide answers grounded in external knowledge.",
        "react": "ReAct combines reasoning and tool actions in an iterative loop.",
    }

    return knowledge.get(
        topic.lower(),
        "No information found for this topic."
    )