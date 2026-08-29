from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from app.ingestion.metadata import extract_metadata
from app.ingestion.parser import AcademicDocumentParser


DATA_DIR = Path.home() / "Desktop/academic-copilot/data"
RESULTS_DIR = Path("evaluation/ingestion/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    pdfs = sorted(DATA_DIR.rglob("*.pdf"))

    representatives = {}

    for pdf_path in pdfs:
        relative_path = pdf_path.relative_to(DATA_DIR)
        subject_folder = relative_path.parts[0]

        representatives.setdefault(
            subject_folder,
            pdf_path,
        )

    print(f"PDFs found          : {len(pdfs)}")
    print(f"Subjects found      : {len(representatives)}")
    print(f"Representatives     : {len(representatives)}")

    parser = AcademicDocumentParser()

    results = []

    for index, (subject_folder, pdf_path) in enumerate(
        sorted(representatives.items()),
        start=1,
    ):
        relative_path = pdf_path.relative_to(DATA_DIR)

        print(
            f"[{index}/{len(representatives)}] "
            f"{relative_path}"
        )

        try:
            markdown = parser.parse(pdf_path)
            metadata = extract_metadata(markdown)

            result = {
                "file": str(relative_path),
                "subject_folder": subject_folder,
                "status": "success",
                "metadata": {
                    "subject": metadata.subject,
                    "course_code": metadata.course_code,
                    "programme": metadata.programme,
                    "semester": metadata.semester,
                    "credits": metadata.credits,
                    "teaching_hours": metadata.teaching_hours,
                },
            }

        except Exception as exc:
            result = {
                "file": str(relative_path),
                "subject_folder": subject_folder,
                "status": "error",
                "error": str(exc),
            }

        results.append(result)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    output_path = (
        RESULTS_DIR / "metadata_validation.json"
    )

    output_path.write_text(
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
        if result["status"] == "success"
    ]

    errors = [
        result
        for result in results
        if result["status"] == "error"
    ]

    def extracted(field: str) -> int:
        return sum(
            result["metadata"].get(field) is not None
            for result in successful
        )

    print()
    print("=" * 80)
    print("METADATA VALIDATION SUMMARY")
    print("=" * 80)

    print(
        f"Successful parsing : "
        f"{len(successful)}/{len(results)}"
    )

    print(
        f"Parsing errors     : "
        f"{len(errors)}"
    )

    print()

    fields = [
        "subject",
        "course_code",
        "programme",
        "semester",
        "credits",
        "teaching_hours",
    ]

    for field in fields:
        count = extracted(field)

        print(
            f"{field:16}: "
            f"{count:2}/{len(successful)} "
            f"({count / len(successful) * 100:.1f}%)"
            if successful
            else
            f"{field:16}: 0/0"
        )

    if errors:
        print()
        print("Parsing errors:")

        for result in errors:
            print(
                f"- {result['file']}: "
                f"{result['error']}"
            )

    print()
    print(
        f"Results saved to: "
        f"{output_path.resolve()}"
    )


if __name__ == "__main__":
    main()
