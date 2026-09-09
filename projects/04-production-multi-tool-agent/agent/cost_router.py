from agent.models import strong_model, cheap_model
from observability.llm import invoke_with_tracking
from observability.usage import calculate_cost

MODEL_NAMES = {
    "cheap": "openai/gpt-oss-20b",
    "strong": "openai/gpt-oss-120b",
}


def choose_model(query: str) -> str:
    response = strong_model.invoke(
        f"""
        Choose the appropriate model for this request.

        Return ONLY one word:

        cheap
        or
        strong

        Use cheap for:
        - simple questions
        - calculations
        - short explanations
        - straightforward tasks

        Use strong for:
        - complex reasoning
        - detailed analysis
        - multi-step problems
        - architecture/design
        - difficult coding tasks

        User request:
        {query}
"""
    )

    decision = response.content.strip().lower()

    if "strong" in decision:
        return "strong"

    return "cheap"



def run_with_routing(query: str):
    decision = choose_model(query)

    model = strong_model if decision == "strong" else cheap_model
    model_name = MODEL_NAMES[decision]

    response, metrics = invoke_with_tracking(
        model,
        model_name,
        query,
    )

    strong_cost = calculate_cost(
        "openai/gpt-oss-120b",
        metrics["input_tokens"],
        metrics["output_tokens"],
    )

    metrics["always_strong_cost_usd"] = strong_cost
    metrics["savings_usd"] = round(
        strong_cost - metrics["cost_usd"],
        6,
    )

    return response, metrics