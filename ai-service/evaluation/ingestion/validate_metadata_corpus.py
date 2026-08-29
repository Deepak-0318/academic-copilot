from __future__ import annotations

import json
from pathlib import Path

from app.ingestion.metadata import extract_metadata
from app.ingestion.parser import AcademicDocumentParser


DATA_DIR = Path.home() / "Desktop/academic-copilot/data"
RESULTS_DIR = Path("evaluation/ingestion/results")
SAMPLES_DIR = RESULTS_DIR / "metadata_samples"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)


def main() -> None:
    pdfs = sorted(DATA_DIR.rglob("*.pdf"))

    # One representative PDF per subject.
    representatives: dict[str, Path] = {}

    for pdf_path in pdfs:
        subject_folder = pdf_path.relative_to(DATA_DIR).parts[0]
        representatives.setdefault(subject_folder, pdf_path)

    print(f"Total PDFs       : {len(pdfs)}")
    print(f"Representative PDFs: {len(representatives)}")
    print()

    parser = AcademicDocumentParser()

    results = []

    for index, (subject_folder, pdf_path) in enumerate(
        sorted(representatives.items()),
        start=1,
    ):
        print(
            f"[{index}/{len(representatives)}] "
            f"Parsing {subject_folder}/{pdf_path.name}"
        )

        try:
            markdown = parser.parse(pdf_path)

            metadata = extract_metadata(markdown)

            sample_path = (
                SAMPLES_DIR
                / f"{subject_folder}.md"
            )

            sample_path.write_text(
                markdown,
                encoding="utf-8",
            )

            results.append(
                {
                    "subject_folder": subject_folder,
                    "file": str(
                        pdf_path.relative_to(DATA_DIR)
                    ),
                    "status": "ok",
                    "subject": metadata.subject,
                    "course_code": metadata.course_code,
                    "programme": metadata.programme,
                    "semester": metadata.semester,
                    "credits": metadata.credits,
                    "teaching_hours": metadata.teaching_hours,
                }
            )

        except Exception as exc:
            results.append(
                {
                    "subject_folder": subject_folder,
                    "file": str(
                        pdf_path.relative_to(DATA_DIR)
                    ),
                    "status": "error",
                    "error": repr(exc),
                }
            )

            print(f"  ERROR: {exc}")

    output_path = (
        RESULTS_DIR / "metadata_corpus.json"
    )

    output_path.write_text(
        json.dumps(
            results,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print()
    print("=" * 80)
    print("METADATA CORPUS VALIDATION")
    print("=" * 80)

    successful = [
        item
        for item in results
        if item["status"] == "ok"
    ]

    failed = [
        item
        for item in results
        if item["status"] == "error"
    ]

    print(f"Subjects tested : {len(results)}")
    print(f"Successful      : {len(successful)}")
    print(f"Failed          : {len(failed)}")

    print()
    print("Field coverage:")

    fields = [
        "subject",
        "course_code",
        "programme",
        "semester",
        "credits",
        "teaching_hours",
    ]

    for field in fields:
        present = sum(
            1
            for item in successful
            if item.get(field) is not None
        )

        total = len(successful)

        percentage = (
            (present / total) * 100
            if total
            else 0
        )

        print(
            f"  {field:15} "
            f"{present:2}/{total:<2} "
            f"({percentage:6.2f}%)"
        )

    if failed:
        print()
        print("Failed documents:")

        for item in failed:
            print(
                f"  {item['subject_folder']}: "
                f"{item['error']}"
            )

    print()
    print(
        f"Results saved to: "
        f"{output_path.resolve()}"
    )


if __name__ == "__main__":
    main()
