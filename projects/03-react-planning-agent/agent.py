from langchain.agents import create_agent
from langchain_groq import ChatGroq

from tools import calculator, search_knowledge


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

tools = [
    calculator,
    search_knowledge,
]

agent = create_agent(
    model=llm,
    tools=tools,
)


def critique_answer(question: str, answer: str) -> str:
    prompt = f"""
        You are reviewing an agent's answer.

        Question:
        {question}

        Answer:
        {answer}

        Check:
        1. Did the answer address the complete question?
        2. Is it consistent with the available information?
        3. Is anything important missing?

        Return only:
        PASS
        or
        RETRY
        """

    response = llm.invoke(prompt)

    return response.content.strip().upper()