from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NOVALENSE"
    app_version: str = "0.1.0"
    debug: bool = True

    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    top_k_default: int = 5

    semantic_weight: float = 0.5
    paraphrase_weight: float = 0.3
    ai_weight: float = 0.2

    sentence_similarity_threshold: float = 0.72
    paraphrase_threshold: float = 0.78
    ai_likelihood_threshold: float = 0.60

    base_dir: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = base_dir / "data"
    raw_papers_dir: Path = data_dir / "raw_papers"
    sample_inputs_dir: Path = data_dir / "sample_inputs"
    outputs_dir: Path = base_dir / "outputs"
    reports_dir: Path = outputs_dir / "reports"
    logs_dir: Path = outputs_dir / "logs"
    index_dir: Path = base_dir / "index"

    faiss_index_path: Path = index_dir / "faiss_index.bin"
    embeddings_path: Path = index_dir / "paper_embeddings.npy"
    id_mapping_path: Path = index_dir / "id_mapping.json"
    corpus_metadata_path: Path = data_dir / "corpus_metadata.csv"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


def ensure_directories() -> None:
    for path in [
        settings.raw_papers_dir,
        settings.sample_inputs_dir,
        settings.outputs_dir,
        settings.reports_dir,
        settings.logs_dir,
        settings.index_dir,
    ]:
        path.mkdir(parents=True, exist_ok=True)
