from dataclasses import dataclass


MODEL_PRICING = {
    "openai/gpt-oss-20b": {
        "input": 0.075,
        "output": 0.30,
    },
    "openai/gpt-oss-120b": {
        "input": 0.15,
        "output": 0.60,
    },
}


@dataclass
class Usage:
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float


def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> float:

    pricing = MODEL_PRICING[model]

    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return input_cost + output_cost


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    return calculate_cost(model, input_tokens, output_tokens)