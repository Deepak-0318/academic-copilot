from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from app.ingestion.service import AcademicIngestionService


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BatchIngestionResult:
    """Summary of a batch ingestion run."""

    total: int
    ingested: int
    duplicates: int
    failed: int
    failures: tuple[dict[str, str], ...]


class AcademicBatchIngestionPipeline:
    """Batch orchestration for academic PDF ingestion."""

    def __init__(
        self,
        ingestion_service: AcademicIngestionService | None = None,
    ) -> None:
        self.ingestion_service = (
            ingestion_service
            or AcademicIngestionService()
        )

    def discover_pdfs(
        self,
        data_dir: str | Path,
    ) -> list[Path]:
        """Discover all PDFs under the corpus directory."""

        root = Path(data_dir).expanduser().resolve()

        if not root.exists():
            raise FileNotFoundError(
                f"Data directory not found: {root}"
            )

        if not root.is_dir():
            raise NotADirectoryError(
                f"Data path is not a directory: {root}"
            )

        return sorted(
            path
            for path in root.rglob("*.pdf")
            if path.is_file()
        )

    def ingest_directory(
        self,
        data_dir: str | Path,
        *,
        university: str | None = None,
        regulation: str | None = None,
        branch: str | None = None,
        document_type: str = "academic_material",
    ) -> BatchIngestionResult:
        """Ingest every PDF under a directory."""

        pdfs = self.discover_pdfs(data_dir)

        logger.info(
            "Starting batch ingestion: directory=%s pdfs=%d",
            Path(data_dir).resolve(),
            len(pdfs),
        )

        ingested = 0
        duplicates = 0
        failures: list[dict[str, str]] = []

        for index, pdf_path in enumerate(
            pdfs,
            start=1,
        ):
            logger.info(
                "Batch progress: %d/%d file=%s",
                index,
                len(pdfs),
                pdf_path.name,
            )

            try:
                result = self.ingestion_service.ingest_pdf(
                    pdf_path,
                    document_type=document_type,
                    university=university,
                    regulation=regulation,
                    branch=branch,
                )

                status = result["status"]

                if status == "ingested":
                    ingested += 1

                elif status == "duplicate":
                    duplicates += 1

                else:
                    raise RuntimeError(
                        f"Unknown ingestion status: {status}"
                    )

            except Exception as exc:
                failure = {
                    "file": str(pdf_path),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                }

                failures.append(failure)

                logger.exception(
                    "Batch document failed: file=%s error=%s",
                    pdf_path,
                    exc,
                )

        result = BatchIngestionResult(
            total=len(pdfs),
            ingested=ingested,
            duplicates=duplicates,
            failed=len(failures),
            failures=tuple(failures),
        )

        logger.info(
            "Batch ingestion completed: total=%d "
            "ingested=%d duplicates=%d failed=%d",
            result.total,
            result.ingested,
            result.duplicates,
            result.failed,
        )

        return result
