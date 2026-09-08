import json
from pathlib import Path

from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_chunk():
    loader = PyMuPDF4LLMLoader(
        "data/attention_all_you_need.pdf"
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    clean_chunks = []

    for i, chunk in enumerate(chunks):
        clean_chunks.append({
            "chunk_id": i,
            "text": chunk.page_content,
            "metadata": {
                "source": "attention_all_you_need.pdf",
                "page": chunk.metadata["page"],
                "document": "Attention Is All You Need",
            },
        })

    return clean_chunks


if __name__ == "__main__":
    chunks = load_and_chunk()

    Path("vector_store").mkdir(exist_ok=True)

    with open("vector_store/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Pages: 15")
    print(f"Chunks: {len(chunks)}")
    print("Chunks saved to vector_store/chunks.json")