from langchain_groq import ChatGroq

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0
)

def process_support_request(message: str) -> str:
    response = llm.invoke(
        f"""
        You are a customer support agent.

        Customer request:
        {message}

        Provide a short helpful response.
        """
    )

    return response.content