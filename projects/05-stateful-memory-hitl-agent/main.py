import sqlite3

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command

from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq

from pydantic import BaseModel
from typing import Literal

from state import SupportState
from tools.orders import get_order
from tools.refunds import process_refund as refund_tool
# -----------------------------
# LLM
# -----------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


# -----------------------------
# Structured Outputs
# -----------------------------

class IssueDetection(BaseModel):
    issue: Literal[
        "damaged_order",
        "wrong_item",
        "missing_item",
        "other",
    ]




issue_llm = llm.with_structured_output(IssueDetection)



# -----------------------------
# Nodes
# -----------------------------

def check_order(state: SupportState):
    order = get_order.invoke({
        "order_id": state["order_id"]
    })

    print("Order:", order)

    if "error" in order:
        return {
            "order": None,
            "issue": "other",
        }

    message = state["messages"][-1].content

    result = issue_llm.invoke(
        f"""
    Identify the customer's issue.

    Customer message:
    {message}
    """
        )

    print("Detected issue:", result.issue)

    return {
        "order": order,
        "issue": result.issue,
    }

def refund_decision(state: SupportState):
    order = state["order"]

    eligible = (
        order["status"] == "delivered"
        and order["item_damaged"] is True
        and order["days_since_delivery"] <= 7
    )

    print("Refund eligible:", eligible)

    if eligible:
        return {
            "refund_requested": True,
            "approval_status": "pending",
        }

    return {
        "refund_requested": False,
        "approval_status": "rejected",
    }

def human_approval(state: SupportState):
    decision = interrupt(
        {
            "message": "Refund requires human approval.",
            "order_id": state["order_id"],
            "reason": state["issue"],
        }
    )

    return {
        "approval_status": decision
    }


def process_refund(state: SupportState):
    print(
        f"Processing refund for order #{state['order_id']}"
    )

    return {
        "messages": [
            AIMessage(
                content=f"Refund processed for order #{state['order_id']}."
            )
        ]
    }

def refund_node(state: SupportState):
    result = refund_tool.invoke({
        "order_id": state["order_id"]
    })

    return {
        "messages": [
            AIMessage(content=result)
        ]
    }

# -----------------------------
# Routing
# -----------------------------

def after_refund_decision(state: SupportState):
    if state["refund_requested"]:
        return "human_approval"

    return END


def after_approval(state: SupportState):
    if state["approval_status"] == "approved":
        return "process_refund"

    return END


# -----------------------------
# Build Graph
# -----------------------------

builder = StateGraph(SupportState)

builder.add_node("check_order", check_order)
builder.add_node("refund_decision", refund_decision)
builder.add_node("human_approval", human_approval)
builder.add_node("process_refund", refund_node)

builder.add_edge(START, "check_order")
builder.add_edge("check_order", "refund_decision")

builder.add_conditional_edges(
    "refund_decision",
    after_refund_decision,
    {
        "human_approval": "human_approval",
        END: END,
    },
)

builder.add_conditional_edges(
    "human_approval",
    after_approval,
    {
        "process_refund": "process_refund",
        END: END,
    },
)

builder.add_edge("process_refund", END)


# -----------------------------
# Persistence
# -----------------------------

connection = sqlite3.connect(
    "checkpoints.db",
    check_same_thread=False,
)

memory = SqliteSaver(connection)

graph = builder.compile(
    checkpointer=memory
)


# -----------------------------
# Conversation
# -----------------------------
def run():
    config = {
        "configurable": {
            "thread_id": "customer-C001"
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

    print("\nGraph paused for human approval.")
    print("\nInterrupt:")
    print(result)

    approval = input("\nApprove refund? (yes/no): ")

    decision = (
        "approved"
        if approval.lower() == "yes"
        else "rejected"
    )

    result = graph.invoke(
        Command(resume=decision),
        config,
    )

    print("\nFinal state:")
    print("Issue:", result["issue"])
    print("Refund requested:", result["refund_requested"])
    print("Approval:", result["approval_status"])

    print("\nConversation:")

    for message in result["messages"]:
        print(
            f"{message.__class__.__name__}: "
            f"{message.content}"
        )


if __name__ == "__main__":
    run()