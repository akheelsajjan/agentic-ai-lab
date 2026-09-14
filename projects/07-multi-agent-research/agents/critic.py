from llm.model import llm


def critic_agent(
    research_results: str,
    technical_results: str,
    industry_results: str,
) -> str:

    response = llm.invoke(
        f"""
You are a research critic.

Review the following research:

General Research:
{research_results}

Technical Analysis:
{technical_results}

Industry Analysis:
{industry_results}

Check for:
- Contradictory information
- Unsupported claims
- Missing important points
- Logical inconsistencies

Provide concise feedback for the final writer.
"""
    )

    return response.content