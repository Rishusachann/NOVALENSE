from app.core.config import settings


class FusionModel:
    def compute_originality(self, semantic_score: float, paraphrase_score: float, ai_score: float) -> float:
        weighted_overlap = (
            settings.semantic_weight * semantic_score
            + settings.paraphrase_weight * paraphrase_score
            + settings.ai_weight * ai_score
        )
        originality = 100 * (1 - min(max(weighted_overlap, 0.0), 1.0))
        return round(originality, 2)
