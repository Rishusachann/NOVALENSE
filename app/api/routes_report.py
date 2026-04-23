from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/v1", tags=["report"])


@router.get("/report")
def get_report(path: str):
    report_path = Path(path)
    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Report not found")
    if report_path.suffix.lower() == ".json":
        return report_path.read_text(encoding="utf-8")
    return {"path": str(report_path.resolve())}
