from __future__ import annotations

from app.retrieval.service import AcademicRetrievalService


QUERIES = [
    {
        "id": "Q012",
        "question": "Which graph traversal techniques are included in the syllabus?",
        "expected_section": "syllabus",
    },
    {
        "id": "Q014",
        "question": "What does CO3 focus on?",
        "expected_section": "co_po_mapping",
    },
    {
        "id": "Q029",
        "question": "What is the assessment plan for Data Structures using C?",
        "expected_section": "assessment",
    },
]


def main() -> None:
    service = AcademicRetrievalService()

    for item in QUERIES:
        print()
        print("=" * 80)
        print(item["id"])
        print(item["question"])
        print(f"Expected section: {item['expected_section']}")
        print("=" * 80)

        results = service.search(
            item["question"],
            limit=20,
            subject="Data Structures using C",
            course_code="CS1083",
        )

        found = False

        for rank, result in enumerate(
            results,
            start=1,
        ):
            section = result.get("section")
            similarity = result.get("similarity")

            marker = ""

            if section == item["expected_section"]:
                marker = "  <-- EXPECTED SECTION"
                found = True

            print(
                f"{rank:2d}. "
                f"section={section!r} "
                f"similarity={similarity:.4f}"
                f"{marker}"
            )

        if not found:
            print(
                "\nExpected section was NOT found "
                "in the top 20 results."
            )


if __name__ == "__main__":
    main()