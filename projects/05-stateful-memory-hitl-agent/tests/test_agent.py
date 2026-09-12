import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.orders import get_order
from tools.refunds import process_refund
from langchain_core.messages import HumanMessage
from unittest.mock import patch
from langgraph.types import Command
from main import graph


def test_existing_order():
    result = get_order.invoke({
        "order_id": "1234"
    })

    assert result["status"] == "delivered"
    assert result["item_damaged"] is True


def test_missing_order():
    result = get_order.invoke({
        "order_id": "9999"
    })

    assert "error" in result


def test_refund_tool():
    result = process_refund.invoke({
        "order_id": "1234"
    })

    assert "successfully processed" in result

def test_refund_approved():
    config = {
        "configurable": {
            "thread_id": "test-approved"
        }
    }

    state = {
        "messages": [
            HumanMessage(
                content="My order #1234 arrived damaged. I want a refund."
            )
        ],
        "customer_id": "C001",
        "order_id": "1234",
        "issue": None,
        "order": None,
        "refund_requested": False,
        "approval_status": None,
    }

    result = graph.invoke(state, config)

    result = graph.invoke(
        Command(resume="approved"),
        config
    )

    assert result["approval_status"] == "approved"


def test_refund_rejected():
    config = {
        "configurable": {
            "thread_id": "test-rejected"
        }
    }

    state = {
        "messages": [
            HumanMessage(
                content="My order #1234 arrived damaged. I want a refund."
            )
        ],
        "customer_id": "C001",
        "order_id": "1234",
        "issue": None,
        "order": None,
        "refund_requested": False,
        "approval_status": None,
    }

    graph.invoke(state, config)

    result = graph.invoke(
        Command(resume="rejected"),
        config
    )

    assert result["approval_status"] == "rejected"