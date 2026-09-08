from sentence_transformers import SentenceTransformer
from sympy import true

_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def embed_text(text: str) ->list[str]:
    return _model.encode(text, normalize_embeddings= True).tolist()

def embed_batch(texts: list[str]) -> list[list[float]]:
    return _model.encode(texts, normalize_embeddings= True).tolist()