from xmlrpc import client

from google import genai
from app.config import settings
from app.embeddings import embed_text
from app.vector_store import search_similar_chunks

client = genai.Client(
    api_key=settings.gemini_api_key
)


SYSTEM_PROMPT = (
    "You are a fintech knowledge assistant. Answer the user's question "
    "using ONLY the provided context. If the context doesn't contain "
    "enough information to answer, say so clearly instead of guessing."
)


def answer_question(question: str, top_k: int = 5) -> dict:
    query_embedding = embed_text(question)
    chunks = search_similar_chunks(query_embedding, top_k=top_k)

    if not chunks:
        return {
            "answer": "I don't have any relevant documents to answer that yet.",
            "sources": [],
        }

    context = "\n\n---\n\n".join(
        f"[Source: {c['file_name']}, Page {c['page_number']}]\n{c['content']}"
        for c in chunks
    )

    user_message = f"Context:\n{context}\n\nQuestion: {question}"

    response = client.models.generate_content(
        model=settings.model_name,  # e.g. "gemini-2.0-flash"
        contents=user_message,
        config={"system_instruction": SYSTEM_PROMPT, "temperature": 0.2, "max_output_tokens": 1000},
    )

    sources = [
        {"file_name": c["file_name"], "page": c["page_number"]} for c in chunks
    ]
    # de-duplicate while preserving order
    seen = set()
    unique_sources = []
    for s in sources:
        key = (s["file_name"], s["page"])
        if key not in seen:
            seen.add(key)
            unique_sources.append(s)

    return {"answer": response.content[0].text, "sources": unique_sources}