import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from models import FlightRequest

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

structured_llm = llm.with_structured_output(FlightRequest)