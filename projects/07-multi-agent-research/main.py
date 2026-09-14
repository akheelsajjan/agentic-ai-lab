from graph.workflow import graph
from evaluation.evaluator import evaluate_answer

query = input("Enter your research question: ")

result = graph.invoke({
    "query":query,
    "research_results": "",
    "technical_results": "",
    "industry_results": "",
    "critic_feedback": "",
    "final_answer": "",
})

print("\n--- Final Answer ---")
final_answer = result["final_answer"]
print(final_answer)

evaluation = evaluate_answer(
    query,
    final_answer,
)

print("\n--- Evaluation ---")
print(evaluation)