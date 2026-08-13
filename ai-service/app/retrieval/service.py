from __future__ import annotations

from typing import Any

from app.db.repository import DocumentRepository
from app.db.session import SessionLocal
from app.embeddings.bge import BGEEmbeddingService
from app.retrieval.query_intent import classify_query


SECTION_BONUS = 0.15
CANDIDATE_LIMIT = 20


class AcademicRetrievalService:
    """Semantic and intent-aware retrieval over academic documents."""

    def __init__(self) -> None:
        self.embedding_service = BGEEmbeddingService()

    def search(
        self,
        query: str,
        *,
        limit: int = 5,
        subject: str | None = None,
        course_code: str | None = None,
        semester: int | None = None,
        university: str | None = None,
        regulation: str | None = None,
        branch: str | None = None,
        document_type: str | None = None,
    ) -> list[dict[str, Any]]:
        if not query.strip():
            raise ValueError("Query cannot be empty.")

        if limit <= 0:
            raise ValueError("Limit must be greater than zero.")

        query_embedding = self.embedding_service.embed_text(
            query
        )

        intent = classify_query(query)

        candidate_limit = max(
            limit,
            CANDIDATE_LIMIT,
        )

        db = SessionLocal()

        try:
            repository = DocumentRepository(db)

            results = repository.search_similar_chunks(
                query_embedding,
                limit=candidate_limit,
                subject=subject,
                course_code=course_code,
                semester=semester,
                university=university,
                regulation=regulation,
                branch=branch,
                document_type=document_type,
            )

            ranked_results = []

            for chunk, distance in results:
                similarity = 1.0 - distance

                section_bonus = (
                    SECTION_BONUS
                    if (
                        intent.preferred_section
                        and chunk.section
                        == intent.preferred_section
                    )
                    else 0.0
                )

                ranked_results.append(
                    {
                        "chunk_id": str(chunk.id),
                        "document_id": str(chunk.document_id),
                        "chunk_index": chunk.chunk_index,
                        "section": chunk.section,
                        "content": chunk.content,
                        "metadata": chunk.metadata_,
                        "distance": distance,
                        "similarity": similarity,
                        "section_bonus": section_bonus,
                        "intent_score": (
                            similarity + section_bonus
                        ),
                    }
                )

            ranked_results.sort(
                key=lambda result: result["intent_score"],
                reverse=True,
            )

            return ranked_results[:limit]

        finally:
            db.close()
