from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    file_path: str = Field(..., description="Absolute or project-relative file path")
    top_k: int = Field(default=5, ge=1, le=20)
    semantic_threshold: float | None = Field(default=None, ge=0.0, le=1.0)
    paraphrase_threshold: float | None = Field(default=None, ge=0.0, le=1.0)
