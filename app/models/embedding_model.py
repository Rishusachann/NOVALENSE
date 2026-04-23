from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.core.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    return SentenceTransformer(settings.model_name)


def encode_texts(texts: list[str]):
    model = get_embedding_model()
    return model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
