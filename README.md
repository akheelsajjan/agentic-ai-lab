# Project 01: Structured Output Agent

Goal : A given query to LLM should generate Structured output 

User Input → LLM → Structured Output → Pydantic Validation → FlightRequest


# Project 02: RAG Agent with Citation Grounding

Goal : Retrieve context, generate answers with sources, flag low-confidence responses, fallback to search.

   User Query
       ↓
    Embedding
       ↓
    FAISS Top-K Retrieval
        ↓
   Evidence Check
        ↓
   ┌───────────────┐
   YES             NO
   ↓                ↓
  Generate        Fallback
  Answer
   ↓
  Citations
