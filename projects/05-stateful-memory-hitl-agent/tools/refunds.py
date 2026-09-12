from langchain_core.tools import tool
failed_once = False

@tool
def process_refund(order_id: str) -> str:
    """Process a refund for an order."""

    print(f"Refund API called for order #{order_id}")

    return f"Refund successfully processed for order #{order_id}."