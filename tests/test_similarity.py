from app.services.similarity_engine import document_similarity_score


def test_document_similarity_score_nonzero_for_related_texts():
    score = document_similarity_score(
        "semantic similarity in academic text",
        ["semantic similarity is used for scholarly comparison"],
    )
    assert score > 0
