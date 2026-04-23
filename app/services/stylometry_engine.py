from __future__ import annotations
from collections import Counter
import numpy as np
from textstat import textstat
from app.services.preprocessing import split_sentences


def _word_tokens(text: str) -> list[str]:
    cleaned = []
    for token in text.split():
        t = token.strip(".,;:!?()[]{}\"'`“”’")
        if t:
            cleaned.append(t.lower())
    return cleaned


def extract_stylometric_features(text: str) -> dict[str, float]:
    sentences = split_sentences(text)
    words = [w for w in _word_tokens(text) if w]
    if not words:
        return {
            "avg_sentence_length": 0.0,
            "sentence_length_variance": 0.0,
            "lexical_diversity": 0.0,
            "repetition_ratio": 0.0,
            "readability": 0.0,
            "entropy": 0.0,
        }

    sentence_lengths = np.array([len(_word_tokens(s)) for s in sentences if s.strip()] or [0])
    lexical_diversity = len(set(words)) / max(len(words), 1)
    repetition_ratio = 1.0 - lexical_diversity
    counts = Counter(words)
    probs = np.array([c / len(words) for c in counts.values()], dtype=float)
    entropy = float(-(probs * np.log2(probs + 1e-12)).sum())

    return {
        "avg_sentence_length": float(sentence_lengths.mean()),
        "sentence_length_variance": float(sentence_lengths.var()),
        "lexical_diversity": float(lexical_diversity),
        "repetition_ratio": float(repetition_ratio),
        "readability": float(textstat.flesch_reading_ease(text)),
        "entropy": entropy,
    }


def ai_likelihood_from_features(features: dict[str, float]) -> tuple[float, list[str]]:
    score = 0.0
    explanations: list[str] = []

    variance = features["sentence_length_variance"]
    diversity = features["lexical_diversity"]
    repetition = features["repetition_ratio"]
    entropy = features["entropy"]
    avg_len = features["avg_sentence_length"]
    readability = features["readability"]

    if variance < 18:
        score += 0.22
        explanations.append("Low sentence-length variance suggests unusually uniform writing flow.")
    if diversity < 0.55:
        score += 0.22
        explanations.append("Lexical diversity is relatively low, indicating repeated phrasing patterns.")
    if repetition > 0.45:
        score += 0.18
        explanations.append("Repetition ratio is elevated compared with typical human-edited academic prose.")
    if entropy < 6.5:
        score += 0.18
        explanations.append("Token entropy is compressed, which can indicate high-probability generation patterns.")
    if 14 <= avg_len <= 24:
        score += 0.10
        explanations.append("Sentence lengths are tightly centered in a generation-friendly range.")
    if readability > 20:
        score += 0.10
        explanations.append("Readability remains smooth and uniform across the text.")

    return min(round(score, 4), 1.0), explanations or ["No dominant stylometric irregularity was detected."]
