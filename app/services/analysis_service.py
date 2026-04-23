from __future__ import annotations
from pathlib import Path
from app.core.config import settings
from app.models.ai_detector import AIDetector
from app.models.fusion_model import FusionModel
from app.schemas.response_schema import AnalyzeResponse, SimilarPaper, FlaggedSentence
from app.services.explanation_engine import build_sentence_explanation
from app.services.paraphrase_engine import aggregate_paraphrase_score, estimate_paraphrase_probability
from app.services.preprocessing import normalize_text, split_sentences
from app.services.report_generator import save_report
from app.services.retrieval_engine import RetrievalEngine
from app.services.similarity_engine import document_similarity_score, sentence_level_matches
from app.services.text_extractor import extract_text


class AnalysisService:
    def __init__(self) -> None:
        self.retrieval_engine = RetrievalEngine()
        self.ai_detector = AIDetector()
        self.fusion_model = FusionModel()

    def analyze(self, file_path: str, top_k: int = 5, semantic_threshold: float | None = None) -> AnalyzeResponse:
        path = Path(file_path)
        raw_text = extract_text(path)
        normalized_text = normalize_text(raw_text)
        input_sentences = split_sentences(normalized_text)

        top_similar = self.retrieval_engine.search(normalized_text, top_k=top_k)
        reference_texts = [item["abstract"] for item in top_similar if item.get("abstract")]
        semantic_score = round(document_similarity_score(normalized_text, reference_texts), 4)

        threshold = semantic_threshold or settings.sentence_similarity_threshold
        flagged = []
        for paper in top_similar:
            reference_sentences = split_sentences(paper["abstract"])
            matches = sentence_level_matches(input_sentences, reference_sentences, threshold=threshold)
            for match in matches:
                paraphrase_probability = estimate_paraphrase_probability(
                    match["input_sentence"],
                    match["matched_sentence"],
                    match["similarity"],
                )
                flagged.append(
                    {
                        **match,
                        "matched_paper_title": paper["title"],
                        "paraphrase_probability": paraphrase_probability,
                        "explanation": build_sentence_explanation(match["similarity"], paraphrase_probability),
                    }
                )

        # Deduplicate by sentence index, keeping strongest match.
        dedup = {}
        for item in flagged:
            idx = item["sentence_index"]
            if idx not in dedup or item["similarity"] > dedup[idx]["similarity"]:
                dedup[idx] = item
        flagged = sorted(dedup.values(), key=lambda x: x["similarity"], reverse=True)

        paraphrase_score = aggregate_paraphrase_score(flagged)
        ai_score, ai_features, ai_explanations = self.ai_detector.predict(normalized_text)
        originality = self.fusion_model.compute_originality(semantic_score, paraphrase_score, ai_score)

        payload = {
            "document_name": path.name,
            "originality_score": originality,
            "module_scores": {
                "semantic_similarity_score": semantic_score,
                "paraphrase_score": paraphrase_score,
                "ai_likelihood_score": ai_score,
                "ai_features": ai_features,
            },
            "top_similar_papers": top_similar,
            "flagged_sentences": flagged,
            "ai_explanations": ai_explanations,
        }
        report_json_path, report_html_path = save_report(payload)

        return AnalyzeResponse(
            document_name=path.name,
            originality_score=originality,
            semantic_similarity_score=semantic_score,
            paraphrase_score=paraphrase_score,
            ai_likelihood_score=ai_score,
            ai_explanations=ai_explanations,
            top_similar_papers=[
                SimilarPaper(
                    paper_id=item["paper_id"],
                    title=item["title"],
                    score=item["score"],
                    year=item.get("year"),
                    source=item.get("source"),
                )
                for item in top_similar
            ],
            flagged_sentences=[
                FlaggedSentence(
                    sentence_index=item["sentence_index"],
                    input_sentence=item["input_sentence"],
                    matched_paper_title=item["matched_paper_title"],
                    matched_sentence=item["matched_sentence"],
                    similarity=item["similarity"],
                    paraphrase_probability=item["paraphrase_probability"],
                    explanation=item["explanation"],
                )
                for item in flagged
            ],
            report_json_path=report_json_path,
            report_html_path=report_html_path,
        )
