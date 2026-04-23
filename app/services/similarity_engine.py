from __future__ import annotations
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.models.embedding_model import encode_texts


def document_similarity_score(query_text: str, reference_texts: list[str]) -> float:
    if not query_text.strip() or not reference_texts:
        return 0.0
    query_emb = encode_texts([query_text])
    ref_embs = encode_texts(reference_texts)
    sims = cosine_similarity(query_emb, ref_embs)[0]
    return float(np.mean(sims)) if len(sims) else 0.0


def sentence_level_matches(
    input_sentences: list[str],
    reference_sentences: list[str],
    threshold: float,
) -> list[dict]:
    if not input_sentences or not reference_sentences:
        return []
    input_embs = encode_texts(input_sentences)
    ref_embs = encode_texts(reference_sentences)
    sim_matrix = cosine_similarity(input_embs, ref_embs)

    matches = []
    for idx, row in enumerate(sim_matrix):
        best_idx = int(np.argmax(row))
        best_score = float(row[best_idx])
        if best_score >= threshold:
            matches.append(
                {
                    "sentence_index": idx,
                    "input_sentence": input_sentences[idx],
                    "matched_sentence": reference_sentences[best_idx],
                    "similarity": round(best_score, 4),
                }
            )
    return matches
