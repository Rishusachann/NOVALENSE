from pydantic import BaseModel


class ReportPayload(BaseModel):
    document_name: str
    originality_score: float
    module_scores: dict
    top_similar_papers: list[dict]
    flagged_sentences: list[dict]
    ai_explanations: list[str]
