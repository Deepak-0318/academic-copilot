from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models import Document, DocumentChunk


class DocumentRepository:
    """Database operations for documents and their chunks."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_document(
        self,
        *,
        subject: str,
        document_type: str,
        file_name: str,
        content_hash: str,
        file_path: str | None = None,
        course_code: str | None = None,
        university: str | None = None,
        regulation: str | None = None,
        branch: str | None = None,
        semester: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Document:
        document = Document(
            subject=subject,
            course_code=course_code,
            document_type=document_type,
            file_name=file_name,
            file_path=file_path,
            content_hash=content_hash,
            university=university,
            regulation=regulation,
            branch=branch,
            semester=semester,
            metadata_=metadata or {},
        )

        self.db.add(document)
        self.db.flush()

        return document

    def create_document_chunks(
        self,
        *,
        document_id: uuid.UUID,
        chunks: list[dict[str, Any]],
    ) -> list[DocumentChunk]:
        if not chunks:
            return []

        document_chunks = [
            DocumentChunk(
                document_id=document_id,
                chunk_index=chunk["chunk_index"],
                content=chunk["content"],
                page_number=chunk.get("page_number"),
                section=chunk.get("section"),
                metadata_=chunk.get("metadata", {}),
                embedding=chunk.get("embedding"),
            )
            for chunk in chunks
        ]

        self.db.add_all(document_chunks)
        self.db.flush()

        return document_chunks
    
    def get_document_by_content_hash(
        self,
        content_hash: str,
    ) -> Document | None:
        statement = select(Document).where(
            Document.content_hash == content_hash
        )

        return self.db.scalar(statement)
    
    def count_document_chunks(
        self,
        document_id: uuid.UUID,
    ) -> int:
        statement = (
            select(func.count())
            .select_from(DocumentChunk)
            .where(
                DocumentChunk.document_id == document_id
            )
        )
        
        return int(self.db.scalar(statement) or 0)

    def get_document(
        self,
        document_id: uuid.UUID,
    ) -> Document | None:
        statement = select(Document).where(
            Document.id == document_id
        )

        return self.db.scalar(statement)

    def get_document_chunks(
        self,
        document_id: uuid.UUID,
    ) -> list[DocumentChunk]:
        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )

        return list(self.db.scalars(statement).all())
    
    def search_similar_chunks(
        self,
        query_embedding: list[float],
        *,
        limit: int = 5,
        subject: str | None = None,
        course_code: str | None = None,
        semester: int | None = None,
        university: str | None = None,
        regulation: str | None = None,
        branch: str | None = None,
        document_type: str | None = None,
    ) -> list[tuple[DocumentChunk, float]]:
        """
        Retrieve the most semantically similar document chunks.

        Optional metadata filters are applied before vector similarity
        ranking.

        Uses pgvector cosine distance.
        Lower distance means higher similarity.
        """

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        ).label("distance")

        statement = (
            select(DocumentChunk, distance)
            .join(Document)
            .where(DocumentChunk.embedding.is_not(None))
        )

        if subject is not None:
            statement = statement.where(
                Document.subject == subject
            )

        if course_code is not None:
            statement = statement.where(
                Document.course_code == course_code
            )

        if semester is not None:
            statement = statement.where(
                Document.semester == semester
            )

        if university is not None:
            statement = statement.where(
                Document.university == university
            )

        if regulation is not None:
            statement = statement.where(
                Document.regulation == regulation
            )

        if branch is not None:
            statement = statement.where(
                Document.branch == branch
            )

        if document_type is not None:
            statement = statement.where(
                Document.document_type == document_type
            )

        statement = (
            statement
            .order_by(distance)
            .limit(limit)
        )

        results = self.db.execute(statement).all()

        return [
            (chunk, float(distance_value))
            for chunk, distance_value in results
        ]