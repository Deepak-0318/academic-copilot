from __future__ import annotations

from functools import lru_cache

from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """Load and cache the embedding model."""

    return SentenceTransformer(MODEL_NAME)


class BGEEmbeddingService:
    """Generate embeddings using BGE-small."""

    def __init__(self) -> None:
        self.model = get_model()

    def embed_text(self, text: str) -> list[float]:
        """Generate one normalized embedding."""

        if not text.strip():
            raise ValueError("Cannot embed empty text.")

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for multiple documents."""

        if not texts:
            return []

        if any(not text.strip() for text in texts):
            raise ValueError(
                "Cannot embed empty document text."
            )

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()