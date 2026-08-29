from __future__ import annotations

from pathlib import Path

from app.ingestion.chunker import create_chunks
from app.ingestion.metadata import extract_metadata
from app.ingestion.parser import AcademicDocumentParser


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
    parser = AcademicDocumentParser()

    total_chunks = 0
    failures = []

    print("=" * 90)
    print("MULTI-SUBJECT DOCUMENT / CHUNK SCHEMA VALIDATION")
    print("=" * 90)

    for index, subject_folder in enumerate(SUBJECTS, start=1):
        pdfs = sorted(
            (DATA_DIR / subject_folder).glob("*.pdf")
        )

        if not pdfs:
            failures.append(
                (subject_folder, "No PDF found")
            )
            continue

        pdf = pdfs[0]

        print()
        print(f"[{index}/{len(SUBJECTS)}] {subject_folder}")
        print(f"PDF: {pdf.name}")

        try:
            markdown = parser.parse(pdf)

            if not markdown.strip():
                raise ValueError("Parser returned empty Markdown")

            metadata = extract_metadata(markdown)

            if not metadata.subject:
                raise ValueError(
                    "Subject metadata could not be extracted"
                )

            chunks = create_chunks(
                markdown,
                subject=metadata.subject,
                document_id="schema-validation",
                course_code=metadata.course_code,
                semester=metadata.semester,
            )

            if not chunks:
                raise ValueError("No chunks generated")

            for chunk in chunks:
                required = [
                    chunk.chunk_index,
                    chunk.content,
                    chunk.section,
                    chunk.metadata,
                ]

                if any(value is None for value in required):
                    raise ValueError(
                        f"Invalid chunk schema: {chunk}"
                    )

            total_chunks += len(chunks)

            print("  STATUS        : PASS")
            print("  Subject       :", metadata.subject)
            print("  Course code   :", metadata.course_code)
            print("  Semester      :", metadata.semester)
            print("  Credits       :", metadata.credits)
            print("  Teaching hrs  :", metadata.teaching_hours)
            print("  Chunks        :", len(chunks))

        except Exception as exc:
            failures.append(
                (subject_folder, str(exc))
            )
            print("  STATUS        : FAIL")
            print("  ERROR         :", exc)

    print()
    print("=" * 90)
    print("VALIDATION SUMMARY")
    print("=" * 90)
    print(f"Subjects tested : {len(SUBJECTS)}")
    print(f"Total chunks    : {total_chunks}")
    print(f"Passed          : {len(SUBJECTS) - len(failures)}")
    print(f"Failed          : {len(failures)}")

    if failures:
        print()
        print("Failures:")
        for subject, error in failures:
            print(f"  - {subject}: {error}")

        raise SystemExit(1)

    print()
    print("ALL REPRESENTATIVE SUBJECTS PASSED")


if __name__ == "__main__":
    main()
