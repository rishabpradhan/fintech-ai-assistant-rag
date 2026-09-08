from psycopg2._psycopg import cursor

from app.db import get_connection

def insert_chunks(document_id: str, chunks:list[dict]):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            for chuck in chunks:
                cursor.execute(
                    """
                    INSERT INTO document_chunks (document_id, chunk)
                      (document_id, chunk_index, content, page_number, embedding)
                      VALUES (%s, %s, %s, %s, %s)
                    """
                    (
                        document_id,
                        chunks["chunk_index"],
                        chunks["content"],
                        chunks["page_number"],
                        chunks["embedding"]
                    ),
                )
        connection.commit()

    finally:
        connection.close()

def  search_similar_chunks(query_embedding:list[float], top_k : int = 5) -> list[dict]:
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                dc.content,
                dc.page_number,
                dc.file_name,
                1 - (dc.embedding <=> %s) AS similarity
                
                FROM document_chunks dc
                JOIN documents d ON d.id = dc.document_id
                ORDER BY dc.embedding <=> %s
                LIMIT %s              
                """
                (query_embedding, query_embedding, top_k)
            )
            rows = cursor.fetchall()
            return [
                {
                    "content": rows[0],
                    "page_number": rows[1],
                    "file_name": rows[2],
                    "similarity": rows[3]
                }
                for row in rows
            ]
    finally:
        connection.close()