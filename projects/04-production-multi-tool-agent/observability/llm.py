import time

from observability.usage import calculate_cost


def invoke_with_tracking(model, model_name: str, query: str):
    start = time.perf_counter()

    response = model.invoke(query)

    latency = time.perf_counter() - start

    usage = response.usage_metadata

    input_tokens = usage["input_tokens"]
    output_tokens = usage["output_tokens"]
    total_tokens = usage["total_tokens"]

    reasoning_tokens = usage.get(
        "output_token_details", {}
    ).get("reasoning", 0)

    cost = calculate_cost(
        model_name,
        input_tokens,
        output_tokens,
    )

    metrics = {
        "model": model_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "total_tokens": total_tokens,
        "latency_seconds": round(latency, 3),
        "cost_usd": cost,
    }

    return response, metrics



