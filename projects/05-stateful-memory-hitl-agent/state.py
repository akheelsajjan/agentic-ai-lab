from langgraph.graph import MessagesState
from typing import Any

class SupportState(MessagesState):
    customer_id: str | None
    order_id: str | None
    issue: str | None
    refund_requested: bool
    approval_status: str | None
    order: dict[str, Any] | None