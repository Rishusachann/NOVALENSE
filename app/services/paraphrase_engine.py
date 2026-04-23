from __future__ import annotations


def estimate_paraphrase_probability(input_sentence: str, matched_sentence: str, similarity: float) -> float:
    input_words = set(input_sentence.lower().split())
    matched_words = set(matched_sentence.lower().split())
    lexical_overlap = len(input_words & matched_words) / max(len(input_words | matched_words), 1)

    # Higher semantic similarity with lower lexical overlap implies paraphrase tendency.
    paraphrase_score = 0.65 * similarity + 0.35 * (1 - lexical_overlap)
    return round(min(max(paraphrase_score, 0.0), 1.0), 4)


def aggregate_paraphrase_score(flagged_sentences: list[dict]) -> float:
    if not flagged_sentences:
        return 0.0
    scores = [item["paraphrase_probability"] for item in flagged_sentences]
    return round(sum(scores) / len(scores), 4)
