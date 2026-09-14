# FinTech Knowledge Assistant — FastAPI AI Service

Python service responsible for all AI/RAG functionality in the AI-Powered FinTech Knowledge Assistant: document text extraction, chunking, embeddings, vector search, and LLM-based question answering using **Google Gemini**.

This is a learning-oriented, production-styled portfolio project. The full system also includes a Spring Boot backend (auth, users, document metadata) — see that service's README for details.

---

## Architecture Overview

```
                Spring Boot API
                       |
                       v
                FastAPI Service  ◄──── (this service)
                       |
             +---------+---------+
             |                   |
             v                   v
    Document Processing      RAG / Q&A
    (extract, chunk,         (embed question,
     embed, store)            search, generate)
             |                   |
             v                   v
          pgvector          Google Gemini
        (PostgreSQL)
```

FastAPI never talks to end users directly — it's called internally by Spring Boot over HTTP.

---

## Responsibilities

- PDF text extraction
- Text chunking (with overlap)
- Embedding generation
- Storing and querying vector embeddings in PostgreSQL (`pgvector`)
- Retrieval-Augmented Generation (RAG): retrieving relevant chunks and building context
- Communication with the Gemini API for answer generation
- Returning answers with source citations (file name + page number)

---

## Tech Stack

| Concern | Technology |
|---|---|
| Language / Framework | Python 3.11+, FastAPI |
| LLM | Google Gemini API (`google-genai`) |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`, local, CPU) |
| PDF extraction | `pypdf` |
| Vector store | PostgreSQL + `pgvector` |
| DB driver | `psycopg2` + `pgvector` Python bindings |
| Config | `pydantic-settings` |


---

## Prerequisites

- Python 3.11+
- PostgreSQL 15+ with the `pgvector` extension enabled
- A Google Gemini API key — get one at [Google AI Studio](https://aistudio.google.com/apikey)

---

