from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.document_processor import process_document
from app.rag import answer_question

app = FastAPI(title="FinTech AI Service")


class ProcessDocumentRequest(BaseModel):
    document_id: str
    file_path: str


class ProcessDocumentResponse(BaseModel):
    chunks_created: int


class AskRequest(BaseModel):
    question: str


class SourceDto(BaseModel):
    file_name: str
    page: int | None


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceDto]


@app.post("/ai/process-document", response_model=ProcessDocumentResponse)
def process_document_endpoint(request: ProcessDocumentRequest):
    try:
        count = process_document(request.document_id, request.file_path)
        return ProcessDocumentResponse(chunks_created=count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")


@app.post("/ai/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        result = answer_question(request.question)
        return AskResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM API error: {e}")


@app.get("/health")
def health():
    return {"status": "ok"}