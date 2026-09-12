# stateful-memory-hitl-agent/
│
├── agent/
│   ├── __init__.py
│   └── state.py
│
├── tools/
│   ├── __init__.py
│   ├── orders.py
│   └── refunds.py
│
├── evaluation/
│   └── scenarios.md
│
├── tests/
│   └── test_agent.py
│
├── main.py
├── pyproject.toml
├── .env
├── .gitignore
└── README.md



# Key Concepts

**State**
SupportState carries workflow information such as:
- Customer ID
- Order ID
- Detected issue
- Order information
- Refund status
- Approval status
- Conversation messages

**Memory**
Conversation messages are maintained inside the LangGraph state.

**Persistence**
SQLite checkpointing persists workflow state : This allows a workflow to be associated with a specific conversation.


**Structured Output**
Pydantic structured output is used for issue detection:

**business rules**
Refund eligibility is determined using deterministic rules based on order information.
The LLM interprets the customer's request, but does not make the final business eligibility decision.

**Human-in-the-Loop**
LangGraph interrupt() pauses the workflow before the refund operation.
The human can: approved / rejected


# Example
Customer:
My order #1234 arrived damaged. I want a refund.

        ↓

Issue:
damaged_order

        ↓

Order:
delivered
item_damaged = true
days_since_delivery = 3

        ↓

Refund eligible

        ↓

Human approval

        ↓

Refund processed


# Evaluation
The project includes scenarios covering:
- Successful refund with approval
- Refund rejection
- Missing order
- Unsupported request


# Production Improvements
he following are intentionally left for the larger production platform project:
- PostgreSQL persistence
- Production refund API
- Retry and timeout policies
- Authentication and authorization
- Observability
- Production monitoring
- Deployment
- Advanced evaluation