import json
from unittest import result
from urllib import response

import faiss
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_groq import ChatGroq
from pydantic import BaseModel, Field



# -----------------------------
# Load vector store
# -----------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)



index = faiss.read_index("vector_store/index.faiss")

with open("vector_store/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)


# -----------------------------
# Embedding model
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)


# -----------------------------
# Retrieval
# -----------------------------

def retrieve(query: str, k: int = 3):

    query_vector = np.array(
        [embeddings.embed_query(query)],
        dtype="float32",
    )

    distances, indices = index.search(query_vector, k)

    results = []

    for rank, chunk_index in enumerate(indices[0], start=1):

        chunk = chunks[chunk_index]

        results.append({
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "distance": float(distances[0][rank - 1]),
        })

    return results

def check_evidence(query: str, results: list) -> bool:
    context = "\n\n".join(
        f"[Source {i}]\n{result['text']}"
        for i, result in enumerate(results, start=1)
    )

    prompt = f"""
    You are an evidence checker for a RAG system.

    Question:
    {query}

    Retrieved context:
    {context}

    Determine whether the retrieved context contains enough relevant
    information to answer the question.

    Return ONLY:
    YES
    or
    NO
    """
    response = llm.invoke(prompt)
    return response.content.strip().upper() == "YES"

# -----------------------------
# Retrieval evaluation
# -----------------------------

queries = [
    "Why is the dot product scaled by the square root of dk?",
    "What is multi-head attention?",
    "How does the Transformer use positional encoding?",
    "What is the architecture of GPT-5?",
    "What is the population of France?",
]


def generate_answer(query: str, results: list) -> str:
    context = "\n\n".join(
        f"[Source {i}]\n"
        f"Document: {result['metadata']['document']}\n"
        f"Page: {result['metadata']['page']}\n"
        f"Text: {result['text']}"
        for i, result in enumerate(results, start=1)
    )

    prompt = f"""
Answer the question using ONLY the provided context.

Question:
{query}

Context:
{context}

Rules:
- Do not use outside knowledge.
- Every important claim must have a citation.
- Use citations exactly like [Source 1], [Source 2].
- Only cite sources that support the claim.
- If the context does not contain enough information, say:
  "The provided document does not contain enough information to answer this question."
"""

    

    response = llm.invoke(prompt)
    return response.content

def print_sources(results: list):
    print("\nSOURCES:")

    for i, result in enumerate(results, start=1):
        metadata = result["metadata"]

        print(
            f"[Source {i}] "
            f"{metadata['document']}, "
            f"Page {metadata['page']}, "
            f"Chunk {result['chunk_id']}"
        )


for query in queries:

    print("\n" + "=" * 60)
    print("QUERY:", query)
    print("=" * 60)

    results = retrieve(query)

    evidence = check_evidence(query, results)

    print("Best distance:", results[0]["distance"])
    print("Evidence:", "YES" if evidence else "NO")

    if evidence:
        answer = generate_answer(query, results)

        print("\nANSWER:")
        print(answer)

        print("\nSOURCES:")
        for i, result in enumerate(results, start=1):
            print(
                f"[Source {i}] "
                f"{result['metadata']['document']}, "
                f"Page {result['metadata']['page']}, "
                f"Chunk {result['chunk_id']}"
            )

    else:
        print("\nFALLBACK:")
        print(
            "I couldn't find enough information in the document "
            "to answer this question."
        )


