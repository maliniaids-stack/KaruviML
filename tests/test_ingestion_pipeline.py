from app.ingestion.pipeline import ingest_pdf_directory


def test_ingest_pdf_directory_preserves_sources_and_pages():
    chunks = ingest_pdf_directory("data/sample")

    assert chunks
    assert {chunk["source"] for chunk in chunks} == {
        "8.1. Pipelines and composite estimators — scikit-learn 1.9.1 documentation.pdf",
        "8.3. Preprocessing data ,estimators, classifiers — scikit-learn 1.9.1 documentation.pdf",
    }
    assert all(chunk["page"] >= 1 for chunk in chunks)
    assert all(chunk["text"] for chunk in chunks)