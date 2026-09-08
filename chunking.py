def chunk_text(text: str, chuck_size: int = 1000, overlap: int = 200) -> list[str]:
    if not text.strip():
        return []

    chunks = []
    start = 0
    text_length = len(text)

    while start <text_length:
        end = start + chuck_size
        chunks.append(text[start:end].strip())
        start += chuck_size - overlap

    return [c for c in chunks if c]