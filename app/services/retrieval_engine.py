from __future__ import annotations
import json
from pathlib import Path
import faiss
import numpy as np
import pandas as pd
from app.core.config import settings
from app.core.logger import get_logger
from app.models.embedding_model import encode_texts

logger = get_logger(__name__)


class RetrievalEngine:
    def __init__(self) -> None:
        self.metadata = pd.read_csv(settings.corpus_metadata_path)
        self._ensure_index()
        self.index = faiss.read_index(str(settings.faiss_index_path))
        self.id_mapping = json.loads(Path(settings.id_mapping_path).read_text(encoding="utf-8"))

    def _ensure_index(self) -> None:
        if settings.faiss_index_path.exists() and settings.embeddings_path.exists() and settings.id_mapping_path.exists():
            return
        logger.info("Building FAISS index from corpus metadata.")
        texts = self.metadata["abstract"].fillna("").tolist()
        embeddings = encode_texts(texts).astype("float32")
        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)
        faiss.write_index(index, str(settings.faiss_index_path))
        np.save(settings.embeddings_path, embeddings)
        mapping = {str(i): row["paper_id"] for i, row in self.metadata.iterrows()}
        Path(settings.id_mapping_path).write_text(json.dumps(mapping, indent=2), encoding="utf-8")

    def search(self, query_text: str, top_k: int = 5) -> list[dict]:
        query_embedding = encode_texts([query_text]).astype("float32")
        scores, indices = self.index.search(query_embedding, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            row = self.metadata.iloc[int(idx)]
            results.append(
                {
                    "paper_id": str(row["paper_id"]),
                    "title": str(row["title"]),
                    "abstract": str(row["abstract"]),
                    "year": int(row["year"]) if not pd.isna(row["year"]) else None,
                    "source": str(row["source"]),
                    "score": round(float(score), 4),
                }
            )
        return results
