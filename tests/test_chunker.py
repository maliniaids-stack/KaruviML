from app.ingestion.chunker import chunk_pages


def test_chunk_pages_keeps_source_and_page():
    pages = [
        {
            "source": "sample.pdf",
            "page": 3,
            "text": "a" * 1200,
        }
    ]

    chunks = chunk_pages(pages, chunk_size=500, overlap=100)

    assert len(chunks) == 3
    assert all(chunk["source"] == "sample.pdf" for chunk in chunks)
    assert all(chunk["page"] == 3 for chunk in chunks)
    assert all(len(chunk["text"]) <= 500 for chunk in chunks)