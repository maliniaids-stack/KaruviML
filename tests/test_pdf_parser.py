from pathlib import Path

from app.ingestion.pdf_parser import extract_pdf_pages


def test_extract_pdf_pages_keeps_source_and_page_number():
    filename = (
        "8.1. Pipelines and composite estimators — "
        "scikit-learn 1.9.1 documentation.pdf"
    )
    pdf_path = Path("data/sample") / filename

    pages = extract_pdf_pages(pdf_path)

    assert pages
    assert pages[0]["source"] == pdf_path.name
    assert pages[0]["page"] == 1
    assert pages[0]["text"]