from typing import Literal
from pydantic import BaseModel
from langchain_groq import ChatGroq


class ToolCall(BaseModel):
    id: str
    tool: Literal["calculator", "search", "weather"]
    arguments: dict
    depends_on: list[str] = []


class RouteDecision(BaseModel):
    tool_calls: list[ToolCall]


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

router = llm.with_structured_output(RouteDecision)


def route_query(query: str) -> RouteDecision:
    return router.invoke(
        f"""
        Create an execution plan for the user's request.

        Available tools:

        calculator: Mathematical calculations. Argument: expression
        search: General information and knowledge. Argument: query
        weather: Weather information. Argument: city

        Rules:
        1. Give every tool call a unique id.
        2. If a tool does not depend on another tool, use an empty depends_on list.
        3. If a tool needs another tool's result, put that tool's id in depends_on,
           and reference the result inside arguments using {{id}} as a placeholder.
           Example: expression "2 + {{w1}}" if it depends on tool id "w1".

        User request:
        {query}
        """
    )