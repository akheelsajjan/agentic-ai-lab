from graph.workflow import graph
from evaluation.evaluator import evaluate_answer


scenarios = [
    "Should a banking company use RAG or fine-tuning?",
    "What are the challenges of deploying LLM applications in production?",
]


total_score = 0

for question in scenarios:

    print(f"\n{'=' * 60}")
    print(f"Question: {question}")

    result = graph.invoke({
        "query": question,
        "research_results": "",
        "technical_results": "",
        "industry_results": "",
        "critic_feedback": "",
        "final_answer": "",
    })

    answer = result["final_answer"]

    print("\n--- Final Answer ---")
    print(answer)

    evaluation = evaluate_answer(
        question,
        answer,
    )

    overall = (
        evaluation.relevance
        + evaluation.accuracy
        + evaluation.completeness
    ) / 3

    total_score += overall

    print("\n--- Evaluation ---")
    print(f"Relevance: {evaluation.relevance}/10")
    print(f"Accuracy: {evaluation.accuracy}/10")
    print(f"Completeness: {evaluation.completeness}/10")
    print(f"Overall: {overall:.1f}/10")
    print(f"Feedback: {evaluation.feedback}")


average_score = total_score / len(scenarios)

print(f"\n{'=' * 60}")
print(f"Average Score: {average_score:.1f}/10")