from langchain_groq import ChatGroq


cheap_model = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

strong_model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)