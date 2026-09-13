from app.knowledge.chroma_store import search


def test_chroma_search_returns_result_structure():
    results = search(
        query="Dubai residence",
        n_results=3,
    )

    assert isinstance(results, dict)
    assert "documents" in results
    assert "metadatas" in results
