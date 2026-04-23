def build_sentence_explanation(similarity: float, paraphrase_probability: float) -> str:
    if similarity > 0.90 and paraphrase_probability > 0.75:
        return "High semantic overlap with strong paraphrase indication."
    if similarity > 0.85:
        return "Very strong conceptual alignment with a reference sentence."
    if paraphrase_probability > 0.80:
        return "Likely rewritten content preserving the original intent."
    return "Moderate semantic overlap requiring reviewer verification."
