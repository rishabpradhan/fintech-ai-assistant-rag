from app.db import get_connection


def insert_chunks(document_id: str, chunks: list[dict]):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            for chunk in chunks:
                cursor.execute(
                    """
                    INSERT INTO document_chunks
                      (document_id, chunk_index, content, page_number, embedding)
                      VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        document_id,
                        chunk["chunk_index"],
                        chunk["content"],
                        chunk["page_number"],
                        chunk["embedding"],
                    ),
                )
        connection.commit()
    finally:
        connection.close()


def search_similar_chunks(query_embedding: list[float], top_k: int = 5) -> list[dict]:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    dc.content,
                    dc.page_number,
                    d.file_name,
                    1 - (dc.embedding <=> %s) AS similarity
                FROM document_chunks dc
                JOIN documents d ON d.id = dc.document_id
                ORDER BY dc.embedding <=> %s
                LIMIT %s
                """,
                (query_embedding, query_embedding, top_k),
            )
            rows = cursor.fetchall()
            return [
                {
                    "content": row[0],
                    "page_number": row[1],
                    "file_name": row[2],
                    "similarity": row[3],
                }
                for row in rows
            ]
    finally:
        connection.close()