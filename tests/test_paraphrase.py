from app.services.paraphrase_engine import estimate_paraphrase_probability


def test_paraphrase_probability_range():
    score = estimate_paraphrase_probability(
        "This method compares contextual embeddings.",
        "The approach evaluates embeddings in context.",
        0.84,
    )
    assert 0.0 <= score <= 1.0
