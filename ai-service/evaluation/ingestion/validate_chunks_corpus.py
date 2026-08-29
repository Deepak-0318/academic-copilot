from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from app.ingestion.chunker import create_chunks
from app.ingestion.metadata import extract_metadata
from app.ingestion.parser import AcademicDocumentParser


DATA_DIR = Path.home() / "Desktop/academic-copilot/data"
RESULTS_DIR = Path("evaluation/ingestion/results")
OUTPUT_PATH = RESULTS_DIR / "chunk_quality_corpus.json"

MIN_CHARS = 200
MAX_CHARS = 3000


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    pdfs = sorted(DATA_DIR.rglob("*.pdf"))

    print("=" * 90)
    print("FULL CORPUS CHUNK QUALITY VALIDATION")
    print("=" * 90)
    print(f"PDFs found: {len(pdfs)}")
    print()

    parser = AcademicDocumentParser()

    results: list[dict] = []

    total_chunks = 0
    section_counts: Counter[str] = Counter()

    failures: list[dict] = []

    for index, pdf_path in enumerate(pdfs, start=1):
        relative_path = pdf_path.relative_to(DATA_DIR)

        print(
            f"[{index}/{len(pdfs)}] "
            f"{relative_path}"
        )

        try:
            markdown = parser.parse(pdf_path)

            metadata = extract_metadata(markdown)

            chunks = create_chunks(
                markdown,
                subject=metadata.subject or "unknown",
                course_code=metadata.course_code,
                university=None,
                regulation=None,
                branch=None,
                semester=metadata.semester,
                min_characters=MIN_CHARS,
                max_characters=MAX_CHARS,
            )

            chunk_lengths = [
                len(chunk.content)
                for chunk in chunks
            ]

            document_sections = Counter(
                chunk.section
                for chunk in chunks
            )

            total_chunks += len(chunks)
            section_counts.update(document_sections)

            short_chunks = [
                length
                for length in chunk_lengths
                if length < MIN_CHARS
            ]

            oversized_chunks = [
                length
                for length in chunk_lengths
                if length > MAX_CHARS
            ]

            result = {
                "file": str(relative_path),
                "status": "ok",
                "subject": metadata.subject,
                "course_code": metadata.course_code,
                "semester": metadata.semester,
                "markdown_characters": len(markdown),
                "chunk_count": len(chunks),
                "min_chunk_characters": (
                    min(chunk_lengths)
                    if chunk_lengths
                    else None
                ),
                "max_chunk_characters": (
                    max(chunk_lengths)
                    if chunk_lengths
                    else None
                ),
                "average_chunk_characters": (
                    sum(chunk_lengths) / len(chunk_lengths)
                    if chunk_lengths
                    else None
                ),
                "short_chunk_count": len(short_chunks),
                "oversized_chunk_count": len(oversized_chunks),
                "sections": dict(document_sections),
            }

            results.append(result)

            print(
                f"  chunks={len(chunks):4} "
                f"min={result['min_chunk_characters']} "
                f"max={result['max_chunk_characters']}"
            )

        except Exception as exc:
            error = {
                "file": str(relative_path),
                "status": "error",
                "error": repr(exc),
            }

            results.append(error)
            failures.append(error)

            print(f"  ERROR: {exc}")

    OUTPUT_PATH.write_text(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    successful = [
        result
        for result in results
        if result["status"] == "ok"
    ]

    zero_chunk_documents = [
        result
        for result in successful
        if result["chunk_count"] == 0
    ]

    short_chunk_documents = [
        result
        for result in successful
        if result["short_chunk_count"] > 0
    ]

    oversized_chunk_documents = [
        result
        for result in successful
        if result["oversized_chunk_count"] > 0
    ]

    print()
    print("=" * 90)
    print("CHUNK QUALITY SUMMARY")
    print("=" * 90)

    print(f"PDFs tested             : {len(results)}")
    print(f"Successful               : {len(successful)}")
    print(f"Failed                   : {len(failures)}")
    print(f"Total chunks             : {total_chunks}")
    print(f"Zero-chunk documents     : {len(zero_chunk_documents)}")
    print(
        f"Documents with short chunks"
        f" : {len(short_chunk_documents)}"
    )
    print(
        f"Documents with oversized chunks"
        f" : {len(oversized_chunk_documents)}"
    )

    print()
    print("Section distribution:")

    for section, count in section_counts.most_common():
        print(
            f"  {section:25} {count:6}"
        )

    if zero_chunk_documents:
        print()
        print("ZERO-CHUNK DOCUMENTS:")

        for result in zero_chunk_documents:
            print(f"  - {result['file']}")

    if failures:
        print()
        print("FAILED DOCUMENTS:")

        for failure in failures:
            print(
                f"  - {failure['file']}: "
                f"{failure['error']}"
            )

    print()
    print(f"Results saved to: {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()