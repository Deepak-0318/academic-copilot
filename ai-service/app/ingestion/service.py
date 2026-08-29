from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from app.db.repository import DocumentRepository
from app.db.session import SessionLocal
from app.embeddings.bge import BGEEmbeddingService
from app.ingestion.chunker import create_chunks
from app.ingestion.metadata import extract_metadata
from app.ingestion.parser import AcademicDocumentParser

logger = logging.getLogger(__name__)


def calculate_file_hash(pdf_path: Path) -> str:
    """Calculate the SHA-256 hash of a PDF file."""

    digest = hashlib.sha256()

    with pdf_path.open("rb") as file:
        for block in iter(
            lambda: file.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


class AcademicIngestionService:
    """End-to-end ingestion pipeline for academic documents."""

    def __init__(self) -> None:
        self.parser = AcademicDocumentParser()
        self.embedding_service = BGEEmbeddingService()

    def ingest_pdf(
        self,
        pdf_path: str | Path,
        *,
        document_type: str = "academic_material",
        university: str | None = None,
        regulation: str | None = None,
        branch: str | None = None,
    ) -> dict:
        pdf_path = Path(pdf_path).expanduser().resolve()

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        # ---------------------------------------------------------
        # 1. Calculate content hash
        # ---------------------------------------------------------
        content_hash = calculate_file_hash(pdf_path)

        logger.info(
            "Starting ingestion: file=%s hash=%s",
            pdf_path.name,
            content_hash,
        )

        # ---------------------------------------------------------
        # 2. Open database transaction
        # ---------------------------------------------------------
        db = SessionLocal()

        try:
            repository = DocumentRepository(db)

            # -----------------------------------------------------
            # 3. Check for duplicate document
            # -----------------------------------------------------
            existing_document = (
                repository.get_document_by_content_hash(
                    content_hash
                )
            )

            if existing_document is not None:
                logger.info(
                    "Skipping duplicate document: file=%s "
                    "existing_document_id=%s",
                    pdf_path.name,
                    existing_document.id,
                )

                return {
                    "status": "duplicate",
                    "document_id": str(existing_document.id),
                    "subject": existing_document.subject,
                    "course_code": existing_document.course_code,
                    "semester": existing_document.semester,
                    "chunk_count": repository.count_document_chunks(
                        existing_document.id
                    ),
                }

            # -----------------------------------------------------
            # 4. Parse PDF
            # -----------------------------------------------------
            logger.info(
                "Parsing document: file=%s",
                pdf_path.name,
            )

            markdown = self.parser.parse(pdf_path)

            if not markdown.strip():
                raise ValueError(
                    "Parser returned empty Markdown."
                )

            # -----------------------------------------------------
            # 5. Extract academic metadata
            # -----------------------------------------------------
            metadata = extract_metadata(markdown)

            if not metadata.subject:
                raise ValueError(
                    "Could not extract subject from document."
                )

            # -----------------------------------------------------
            # 6. Create academic-aware chunks before persistence.
            # -----------------------------------------------------
            chunks = create_chunks(
                markdown,
                subject=metadata.subject,
                course_code=metadata.course_code,
                university=university,
                regulation=regulation,
                branch=branch,
                semester=metadata.semester,
            )

            if not chunks:
                raise ValueError(
                    "No valid chunks were generated from the document."
                )

            logger.info(
                "Generated chunks: file=%s chunks=%d",
                pdf_path.name,
                len(chunks),
            )

            # -----------------------------------------------------
            # 7. Generate embeddings before persistence.
            # -----------------------------------------------------
            texts = [chunk.content for chunk in chunks]

            logger.info(
                "Generating embeddings: file=%s chunks=%d",
                pdf_path.name,
                len(chunks),
            )

            embeddings = self.embedding_service.embed_documents(
                texts
            )

            if len(embeddings) != len(chunks):
                raise RuntimeError(
                    "Embedding count does not match chunk count."
                )

            # -----------------------------------------------------
            # 8. Create document record.
            # -----------------------------------------------------
            document = repository.create_document(
                subject=metadata.subject,
                course_code=metadata.course_code,
                document_type=document_type,
                file_name=pdf_path.name,
                file_path=str(pdf_path),
                content_hash=content_hash,
                university=university,
                regulation=regulation,
                branch=branch,
                semester=metadata.semester,
                metadata={
                    "programme": metadata.programme,
                    "credits": metadata.credits,
                    "teaching_hours": metadata.teaching_hours,
                },
            )

            # -----------------------------------------------------
            # 9. Prepare database records
            # -----------------------------------------------------
            chunk_records = []

            for chunk, embedding in zip(
                chunks,
                embeddings,
                strict=True,
            ):
                chunk_records.append(
                    {
                        "chunk_index": chunk.chunk_index,
                        "content": chunk.content,
                        "section": chunk.section,
                        "metadata": {
                            **chunk.metadata,
                            "document_id": str(document.id),
                        },
                        "embedding": embedding,
                    }
                )

            # -----------------------------------------------------
            # 10. Store chunks + embeddings
            # -----------------------------------------------------
            repository.create_document_chunks(
                document_id=document.id,
                chunks=chunk_records,
            )

            # -----------------------------------------------------
            # 11. Commit entire transaction
            # -----------------------------------------------------
            logger.info(
                "Committing document: file=%s document_id=%s "
                "chunks=%d",
                pdf_path.name,
                document.id,
                len(chunks),
            )

            db.commit()

            logger.info(
                "Ingestion successful: file=%s document_id=%s "
                "chunks=%d",
                pdf_path.name,
                document.id,
                len(chunks),
            )

            return {
                "status": "ingested",
                "document_id": str(document.id),
                "subject": metadata.subject,
                "course_code": metadata.course_code,
                "semester": metadata.semester,
                "credits": metadata.credits,
                "teaching_hours": metadata.teaching_hours,
                "chunk_count": len(chunks),
            }

        except Exception:
            db.rollback()

            logger.exception(
                "Ingestion failed: file=%s hash=%s",
                pdf_path.name,
                content_hash,
            )

            raise

        finally:
            db.close()
