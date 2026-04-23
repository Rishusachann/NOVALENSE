from pathlib import Path
import fitz
from docx import Document
from app.core.constants import SUPPORTED_EXTENSIONS


class TextExtractionError(Exception):
    pass


def extract_text(file_path: str | Path) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise TextExtractionError(f"Unsupported file type: {suffix}")
    if not path.exists():
        raise TextExtractionError(f"File not found: {path}")

    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".docx":
        return _extract_docx(path)
    if suffix == ".pdf":
        return _extract_pdf(path)
    raise TextExtractionError(f"Unsupported file type: {suffix}")


def _extract_pdf(path: Path) -> str:
    with fitz.open(path) as doc:
        pages = [page.get_text("text") for page in doc]
    text = "\n".join(pages).strip()
    if not text:
        raise TextExtractionError("No readable text found in PDF")
    return text


def _extract_docx(path: Path) -> str:
    document = Document(path)
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    text = "\n".join(paragraphs).strip()
    if not text:
        raise TextExtractionError("No readable text found in DOCX")
    return text
