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
def test_ingestion_chunk_ids_are_repeatable():
    first_run = ingest_pdf_directory("data/sample")
    second_run = ingest_pdf_directory("data/sample")

    first_ids = [chunk["chunk_id"] for chunk in first_run]
    second_ids = [chunk["chunk_id"] for chunk in second_run]

    assert first_ids == second_ids
    assert len(first_ids) == len(set(first_ids))