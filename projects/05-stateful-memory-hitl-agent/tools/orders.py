from langchain_core.tools import tool


ORDERS = {
    "1234": {
        "status": "delivered",
        "item_damaged": True,
        "days_since_delivery": 3,
    },
    "5678": {
        "status": "delivered",
        "item_damaged": False,
        "days_since_delivery": 10,
    },
}


@tool
def get_order(order_id: str) -> dict:
    """Get order information."""
    return ORDERS.get(
        order_id,
        {"error": "Order not found"},
    )