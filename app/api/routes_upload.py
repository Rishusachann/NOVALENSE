from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.core.config import settings
from app.core.constants import SUPPORTED_EXTENSIONS

router = APIRouter(prefix="/api/v1", tags=["upload"])


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict:
    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    destination = settings.raw_papers_dir / file.filename
    content = await file.read()
    destination.write_bytes(content)
    return {"message": "File uploaded successfully", "file_path": str(destination.resolve())}
