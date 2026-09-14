from pydantic import BaseModel
from llm.model import llm


class EvaluationResult(BaseModel):
    relevance: int
    accuracy: int
    completeness: int
    feedback: str


evaluator = llm.with_structured_output(EvaluationResult)


def evaluate_answer(
    question: str,
    answer: str,
) -> EvaluationResult:

    return evaluator.invoke(
        f"""
Evaluate the answer to the user's question.

Question:
{question}

Answer:
{answer}

Score from 1 to 10:

- relevance
- accuracy
- completeness

Also provide short feedback.
"""
    )