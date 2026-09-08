from pypdf import PdfReader
from yaml import reader

from app.chunking import chunk_text
from app.embeddings import embed_batch
from app.vector_store import insert_chunks

def process_document(document_id: str, file_path: str):
    reader = PdfReader(file_path)

    all_chunks = []
    chunk_index = 0

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        page_chunks = chunk_text(page_text)

        for content in page_chunks:
            all_chunks.append(
                {
                    "chunk_index": chunk_index,
                    "content": content,
                    "page_number": page_number,
                }
            )
            chunk_index += 1

    if not all_chunks:
        return 0

    embeddings = embed_batch([c["content"] for c in all_chunks])
    for chunk, embedding in zip(all_chunks, embeddings):
        chunk["embedding"] = embedding

    insert_chunks(document_id, all_chunks)
    return len(all_chunks)