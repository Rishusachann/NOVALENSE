from app.models.ai_detector import AIDetector


def test_ai_detector_returns_score():
    detector = AIDetector()
    score, features, explanations = detector.predict("This is a simple academic sentence. This is another sentence.")
    assert 0.0 <= score <= 1.0
    assert "lexical_diversity" in features
    assert isinstance(explanations, list)
