from app.services.preprocessing import normalize_text, split_sentences


def test_normalize_text():
    text = "Hello   world\n\nThis is a test."
    assert "  " not in normalize_text(text)


def test_split_sentences():
    sentences = split_sentences("This is one. This is two.")
    assert len(sentences) == 2
