from __future__ import annotations

import json
import logging
from pathlib import Path

from app.ingestion.pipeline import AcademicBatchIngestionPipeline
from app.logging_config import configure_logging


DATA_DIR = Path.home() / "Desktop/academic-copilot/data"
RESULTS_DIR = Path("evaluation/ingestion/results")
REPORT_PATH = RESULTS_DIR / "batch_ingestion_report.json"


def main() -> None:
    configure_logging()

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    pipeline = AcademicBatchIngestionPipeline()

    print("=" * 90)
    print("ACADEMIC CO-PILOT — FULL CORPUS INGESTION")
    print("=" * 90)
    print(f"Data directory: {DATA_DIR}")
    print()

    pdfs = pipeline.discover_pdfs(DATA_DIR)

    print(f"PDFs discovered: {len(pdfs)}")

    if len(pdfs) != 104:
        raise RuntimeError(
            f"Expected 104 PDFs, found {len(pdfs)}."
        )

    print()
    print("Starting ingestion...")
    print("This may take some time because Docling and BGE")
    print("are executed for documents that are not duplicates.")
    print()

    result = pipeline.ingest_directory(
        DATA_DIR,
        university="VTU",
        regulation="2025 Regulation",
        branch="CSE",
    )

    report = {
        "total": result.total,
        "ingested": result.ingested,
        "duplicates": result.duplicates,
        "failed": result.failed,
        "failures": list(result.failures),
    }

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print()
    print("=" * 90)
    print("FULL CORPUS INGESTION SUMMARY")
    print("=" * 90)
    print(f"Total PDFs : {result.total}")
    print(f"Ingested   : {result.ingested}")
    print(f"Duplicates : {result.duplicates}")
    print(f"Failed     : {result.failed}")
    print()
    print(f"Report: {REPORT_PATH.resolve()}")

    if result.failures:
        print()
        print("FAILED DOCUMENTS")

        for failure in result.failures:
            print(f"  File : {failure['file']}")
            print(f"  Error: {failure['error']}")
            print()

        raise SystemExit(1)

    print()
    print("FULL CORPUS INGESTION: SUCCESS")


if __name__ == "__main__":
    main()