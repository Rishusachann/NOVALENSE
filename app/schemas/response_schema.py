from pydantic import BaseModel


class SimilarPaper(BaseModel):
    paper_id: str
    title: str
    score: float
    year: int | None = None
    source: str | None = None


class FlaggedSentence(BaseModel):
    sentence_index: int
    input_sentence: str
    matched_paper_title: str
    matched_sentence: str
    similarity: float
    paraphrase_probability: float
    explanation: str


class AnalyzeResponse(BaseModel):
    document_name: str
    originality_score: float
    semantic_similarity_score: float
    paraphrase_score: float
    ai_likelihood_score: float
    ai_explanations: list[str]
    top_similar_papers: list[SimilarPaper]
    flagged_sentences: list[FlaggedSentence]
    report_json_path: str
    report_html_path: str
