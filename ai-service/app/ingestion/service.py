from __future__ import annotations

from pathlib import Path

from app.db.repository import DocumentRepository
from app.db.session import SessionLocal
from app.embeddings.bge import BGEEmbeddingService
from app.ingestion.chunker import create_chunks
from app.ingestion.metadata import extract_metadata
from app.ingestion.parser import AcademicDocumentParser


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
    ):
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        # ---------------------------------------------------------
        # 1. Parse PDF
        # ---------------------------------------------------------
        markdown = self.parser.parse(pdf_path)

        # ---------------------------------------------------------
        # 2. Extract academic metadata
        # ---------------------------------------------------------
        metadata = extract_metadata(markdown)

        if not metadata.subject:
            raise ValueError(
                "Could not extract subject from document."
            )

        # ---------------------------------------------------------
        # 3. Open database transaction
        # ---------------------------------------------------------
        db = SessionLocal()

        try:
            repository = DocumentRepository(db)

            # -----------------------------------------------------
            # 4. Create document record
            # -----------------------------------------------------
            document = repository.create_document(
                subject=metadata.subject,
                course_code=metadata.course_code,
                document_type=document_type,
                file_name=pdf_path.name,
                file_path=str(pdf_path),
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
            # 5. Create academic-aware chunks
            # -----------------------------------------------------
            chunks = create_chunks(
                markdown,
                subject=metadata.subject,
                document_id=str(document.id),
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

            # -----------------------------------------------------
            # 6. Generate embeddings
            # -----------------------------------------------------
            texts = [chunk.content for chunk in chunks]

            embeddings = self.embedding_service.embed_documents(
                texts
            )

            if len(embeddings) != len(chunks):
                raise RuntimeError(
                    "Embedding count does not match chunk count."
                )

            # -----------------------------------------------------
            # 7. Prepare database records
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
                        "metadata": chunk.metadata,
                        "embedding": embedding,
                    }
                )

            # -----------------------------------------------------
            # 8. Store chunks + embeddings
            # -----------------------------------------------------
            repository.create_document_chunks(
                document_id=document.id,
                chunks=chunk_records,
            )

            # -----------------------------------------------------
            # 9. Commit entire transaction
            # -----------------------------------------------------
            db.commit()

            return {
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
            raise

        finally:
            db.close()