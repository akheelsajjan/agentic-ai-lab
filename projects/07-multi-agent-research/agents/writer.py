from llm.model import llm


def writer_agent(
    query: str,
    research_results: str,
    technical_results: str,
    industry_results: str,
    critic_feedback: str,
) -> str:

    response = llm.invoke(
        f"""
You are the final research writer.

User question:
{query}

General Research:
{research_results}

Technical Analysis:
{technical_results}

Industry Analysis:
{industry_results}

Critic Feedback:
{critic_feedback}

Write a clear and accurate final answer.

Use the critic feedback to improve the answer.
Do not invent information.
"""
    )

    return response.content

