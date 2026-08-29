from __future__ import annotations

from pathlib import Path

from app.ingestion.service import AcademicIngestionService


DATA_DIR = Path.home() / "Desktop/academic-copilot/data"

SUBJECTS = [
    "Data_Structures_using_C",
    "Operating_System",
    "Database_Management_Systems",
    "Computer_Networks",
    "Linear_Algebra",
    "Programming_in_C",
    "Python_Programming_for_Data_Analytics",
    "Machine_Learning_for_Data_science",
    "Deep_Learning",
    "NLP",
]


def main() -> None:
    ingestion = AcademicIngestionService()

    print("=" * 90)
    print("REPRESENTATIVE MULTI-SUBJECT INGESTION")
    print("=" * 90)

    successful = 0
    failures = []

    for index, subject in enumerate(SUBJECTS, start=1):
        pdfs = sorted(
            (DATA_DIR / subject).glob("*.pdf")
        )

        if not pdfs:
            failures.append(
                (subject, "No PDF found")
            )
            continue

        pdf = pdfs[0]

        print()
        print(
            f"[{index}/{len(SUBJECTS)}] "
            f"{subject}"
        )
        print(f"PDF: {pdf.name}")

        try:
            result = ingestion.ingest_pdf(pdf)

            print("STATUS        : PASS")
            print("Document ID   :", result["document_id"])
            print("Subject       :", result["subject"])
            print("Course code   :", result["course_code"])
            print("Semester      :", result["semester"])
            print("Credits       :", result["credits"])
            print("Teaching hrs  :", result["teaching_hours"])
            print("Chunks        :", result["chunk_count"])

            successful += 1

        except Exception as exc:
            failures.append(
                (subject, str(exc))
            )

            print("STATUS        : FAIL")
            print("ERROR         :", exc)

    print()
    print("=" * 90)
    print("INGESTION SUMMARY")
    print("=" * 90)
    print(f"Subjects attempted : {len(SUBJECTS)}")
    print(f"Successful          : {successful}")
    print(f"Failed              : {len(failures)}")

    if failures:
        print()
        print("Failures:")
        for subject, error in failures:
            print(f"  - {subject}: {error}")

        raise SystemExit(1)

    print()
    print("ALL REPRESENTATIVE SUBJECTS INGESTED SUCCESSFULLY")


if __name__ == "__main__":
    main()
