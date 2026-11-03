from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Convert text strings into embedding vectors."""
    if not texts:
        return []

    model = SentenceTransformer(MODEL_NAME)
    vectors = model.encode(texts, normalize_embeddings=True)

    return vectors.tolist()