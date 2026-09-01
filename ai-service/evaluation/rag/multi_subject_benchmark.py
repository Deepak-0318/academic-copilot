from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from app.db.repository import DocumentRepository
from app.db.session import SessionLocal
from app.retrieval.service import AcademicRetrievalService


DATASET = Path("evaluation/rag/datasets/multi_subject.json")
RESULTS_DIR = Path("evaluation/rag/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT = RESULTS_DIR / "multi_subject.json"


ALIASES = {
    "data structures using c": [
        "data structures using c",
    ],
    "operating systems": [
        "operating system",
        "operating systems",
    ],
    "python": [
        "python programming for data analytics",
        "python programming",
        "python",
    ],
    "fundamentals of natural language processing": [
        "nlp",
        "natural language processing",
        "fundamentals of natural language processing",
    ],
    "machine learning for data science": [
        "machine learning for data science",
        "machine learning",
    ],
}


def normalize(value: str | None) -> str:
    if not value:
        return ""

    return (
        " ".join(
            value.lower()
            .replace("_", " ")
            .replace("-", " ")
            .split()
        )
    )


def subject_matches(
    retrieved_subject: str | None,
    expected_subject: str,
) -> bool:
    retrieved = normalize(retrieved_subject)
    expected = normalize(expected_subject)

    if not retrieved:
        return False

    if retrieved == expected:
        return True

    aliases = ALIASES.get(expected, [])

    return any(
        normalize(alias) == retrieved
        for alias in aliases
    )


def build_document_map(repository):
    documents = repository.get_all_documents()

    return {
        str(document.id): document
        for document in documents
    }


def main() -> None:
    with DATASET.open(encoding="utf-8") as file:
        questions = json.load(file)

    retrieval = AcademicRetrievalService()

    db = SessionLocal()

    try:
        repository = DocumentRepository(db)
        documents = build_document_map(repository)

        print("=" * 90)
        print("MULTI-SUBJECT RETRIEVAL BENCHMARK")
        print("=" * 90)
        print(f"Questions : {len(questions)}")
        print(f"Documents : {len(documents)}")

        if not documents:
            raise RuntimeError(
                "No documents found in the database."
            )

        results = []

        for index, question in enumerate(
            questions,
            start=1,
        ):
            query = question["query"]
            expected_subject = question["expected_subject"]

            retrieved = retrieval.search(
                query,
                limit=5,
            )

            ranked_subjects = []

            for item in retrieved:
                document = documents.get(
                    str(item["document_id"])
                )

                ranked_subjects.append(
                    {
                        "document_id": item["document_id"],
                        "chunk_id": item["chunk_id"],
                        "subject": (
                            document.subject
                            if document
                            else None
                        ),
                        "section": item["section"],
                        "similarity": item["similarity"],
                        "intent_score": item["intent_score"],
                    }
                )

            top_subject = (
                ranked_subjects[0]["subject"]
                if ranked_subjects
                else None
            )

            top1_match = subject_matches(
                top_subject,
                expected_subject,
            )

            top5_match = any(
                subject_matches(
                    item["subject"],
                    expected_subject,
                )
                for item in ranked_subjects
            )

            result = {
                "id": question["id"],
                "query": query,
                "expected_subject": expected_subject,
                "top_subject": top_subject,
                "top1_match": top1_match,
                "top5_match": top5_match,
                "ranked_results": ranked_subjects,
            }

            results.append(result)

            status = "PASS" if top1_match else "FAIL"

            print(
                f"[{index:02}/{len(questions)}] "
                f"{status} | "
                f"{question['id']} | "
                f"expected={expected_subject} | "
                f"top={top_subject}"
            )

        total = len(results)

        top1_accuracy = (
            sum(
                result["top1_match"]
                for result in results
            )
            / total
            if total
            else 0.0
        )

        top5_hit_rate = (
            sum(
                result["top5_match"]
                for result in results
            )
            / total
            if total
            else 0.0
        )

        failures = [
            result
            for result in results
            if not result["top1_match"]
        ]

        failures_by_subject = Counter(
            result["expected_subject"]
            for result in failures
        )

        output = {
            "total_questions": total,
            "top1_subject_accuracy": top1_accuracy,
            "top5_subject_hit_rate": top5_hit_rate,
            "failure_count": len(failures),
            "failures_by_subject": dict(
                failures_by_subject
            ),
            "results": results,
        }

        OUTPUT.write_text(
            json.dumps(
                output,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        print()
        print("=" * 90)
        print("BENCHMARK SUMMARY")
        print("=" * 90)
        print(
            f"Top-1 subject accuracy : "
            f"{top1_accuracy:.4f}"
        )
        print(
            f"Top-5 subject hit rate : "
            f"{top5_hit_rate:.4f}"
        )
        print(f"Failures               : {len(failures)}")
        print(f"Results                : {OUTPUT}")

        if failures:
            print()
            print("FAILURES")
            print("-" * 90)

            for failure in failures:
                print(
                    f"{failure['id']} | "
                    f"expected={failure['expected_subject']} | "
                    f"top={failure['top_subject']} | "
                    f"query={failure['query']}"
                )

    finally:
        db.close()


if __name__ == "__main__":
    main()
