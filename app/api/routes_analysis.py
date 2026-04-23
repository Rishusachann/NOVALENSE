from fastapi import APIRouter, HTTPException
from app.schemas.request_schema import AnalyzeRequest
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api/v1", tags=["analysis"])
service = AnalysisService()


@router.post("/analyze")
def analyze_document(request: AnalyzeRequest):
    try:
        return service.analyze(
            file_path=request.file_path,
            top_k=request.top_k,
            semantic_threshold=request.semantic_threshold,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
