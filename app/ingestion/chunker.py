def chunk_pages(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    """Split page text into overlapping chunks, preserving source and page."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []
    step = chunk_size - overlap

    for page in pages:
        text = page["text"].strip()
        for start in range(0, len(text), step):
            chunk_text = text[start : start + chunk_size].strip()
            if chunk_text:
                chunks.append(
                    {
                        "source": page["source"],
                        "page": page["page"],
                        "text": chunk_text,
                    }
                )

    return chunks