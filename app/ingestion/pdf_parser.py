from pathlib import Path

from pypdf import PdfReader


def extract_pdf_pages(pdf_path: str | Path) -> list[dict]:
    """Extract text from a PDF, keeping its file name and page number."""
    path = Path(pdf_path)
    reader = PdfReader(path)

    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if text.strip():
            pages.append(
                {
                    "source": path.name,
                    "page": page_number,
                    "text": text.strip(),
                }
            )

    return pages