from typing import TypedDict


class ResearchState(TypedDict):
    query: str

    research_results: str
    technical_results: str
    industry_results: str

    critic_feedback: str

    final_answer: str