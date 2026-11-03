import hashlib
from pathlib import Path

from app.ingestion.chunker import chunk_pages
from app.ingestion.pdf_parser import extract_pdf_pages


def ingest_pdf(pdf_path: str | Path) -> list[dict]:
    """Extract a PDF and return page-aware chunks with stable IDs."""
    pages = extract_pdf_pages(pdf_path)
    chunks = chunk_pages(pages)

    for chunk in chunks:
        identity = (
            f"{chunk['source']}|{chunk['page']}|{chunk['text']}"
        )
        chunk["chunk_id"] = hashlib.sha256(
            identity.encode("utf-8")
        ).hexdigest()

    return chunks


def ingest_pdf_directory(directory: str | Path) -> list[dict]:
    """Ingest all PDF files in a directory."""
    pdf_files = sorted(Path(directory).glob("*.pdf"))

    chunks = []
    for pdf_path in pdf_files:
        chunks.extend(ingest_pdf(pdf_path))

    return chunks