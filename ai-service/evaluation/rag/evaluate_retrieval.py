from __future__ import annotations

import json
from pathlib import Path
from collections import Counter

from app.retrieval.service import AcademicRetrievalService


DATASET = Path("evaluation/rag/datasets/multi_subject.json")
RESULTS_DIR = Path("evaluation/rag/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def normalize(value: str | None) -> str:
    if not value:
        return ""

    return (
        value
        .lower()
        .replace("_", " ")
        .strip()
    )


def subject_matches(
    retrieved: str | None,
    expected: str,
) -> bool:
    retrieved_norm = normalize(retrieved)
    expected_norm = normalize(expected)

    aliases = {
        "data structures using c": "data structures using c",
        "data structures using c": "data structures using c",

        "operating system": "operating systems",
        "operating systems": "operating systems",

        "machine learning for data science":
            "machine learning for data science",
        "machine learning for data science":
            "machine learning for data science",

        "nlp":
            "fundamentals of natural language processing",
        "fundamentals of natural language processing":
            "fundamentals of natural language processing",

        "python": "python",
    }

    return (
        aliases.get(retrieved_norm, retrieved_norm)
        == aliases.get(expected_norm, expected_norm)
    )


def main() -> None:
    with DATASET.open("r", encoding="utf-8") as f:
        questions = json.load(f)

    service = AcademicRetrievalService()

    results = []

    top1_correct = 0
    top3_correct = 0
    empty_results = 0
    errors = 0

    print("=" * 90)
    print("ACADEMIC RAG RETRIEVAL EVALUATION")
    print("=" * 90)
    print(f"Questions: {len(questions)}")
    print()

    for index, item in enumerate(questions, start=1):
        query = item["query"]
        expected = item["expected_subject"]

        try:
            retrieved = service.search(
                query,
                limit=5,
            )
        except Exception as exc:
            errors += 1

            print(
                f"[{index}/{len(questions)}] ERROR | "
                f"{item['id']} | {exc}"
            )

            results.append(
                {
                    **item,
                    "error": str(exc),
                    "top1_subject": None,
                    "top3_subjects": [],
                    "top1_correct": False,
                    "top3_correct": False,
                }
            )

            continue

        if not retrieved:
            empty_results += 1

            print(
                f"[{index}/{len(questions)}] EMPTY | "
                f"{item['id']} | "
                f"expected={expected}"
            )

            results.append(
                {
                    **item,
                    "top1_subject": None,
                    "top3_subjects": [],
                    "top1_correct": False,
                    "top3_correct": False,
                }
            )

            continue

        top_subjects = []

        for result in retrieved:
            metadata = result.get("metadata") or {}

            subject = metadata.get("subject")

            top_subjects.append(subject or "UNKNOWN")

        top1_subject = top_subjects[0]

        top1_ok = subject_matches(
            top1_subject,
            expected,
        )

        top3_ok = any(
            subject_matches(subject, expected)
            for subject in top_subjects[:3]
        )

        if top1_ok:
            top1_correct += 1

        if top3_ok:
            top3_correct += 1

        result_record = {
            **item,
            "top1_subject": top1_subject,
            "top3_subjects": top_subjects[:3],
            "top1_correct": top1_ok,
            "top3_correct": top3_ok,
            "retrieval": [
                {
                    "chunk_id": result["chunk_id"],
                    "document_id": result["document_id"],
                    "section": result["section"],
                    "subject": (
                        result.get("metadata") or {}
                    ).get("subject"),
                    "course_code": (
                        result.get("metadata") or {}
                    ).get("course_code"),
                    "similarity": result["similarity"],
                    "intent_score": result["intent_score"],
                }
                for result in retrieved
            ],
        }

        results.append(result_record)

        status = "PASS" if top1_ok else "FAIL"

        print(
            f"[{index}/{len(questions)}] {status} | "
            f"{item['id']} | "
            f"expected={expected} | "
            f"top1={top1_subject}"
        )

    total = len(questions)

    print()
    print("=" * 90)
    print("RETRIEVAL EVALUATION SUMMARY")
    print("=" * 90)

    print(f"Total questions : {total}")
    print(f"Top-1 correct   : {top1_correct}")
    print(f"Top-3 correct   : {top3_correct}")
    print(f"Empty results   : {empty_results}")
    print(f"Errors          : {errors}")

    if total:
        print(
            f"Top-1 accuracy  : "
            f"{top1_correct / total:.2%}"
        )

        print(
            f"Top-3 accuracy  : "
            f"{top3_correct / total:.2%}"
        )

    failures = [
        result
        for result in results
        if not result.get("top1_correct", False)
        and "error" not in result
    ]

    print()
    print("Failures:")

    if not failures:
        print("  None")
    else:
        for failure in failures:
            print(
                f"  {failure['id']} | "
                f"expected={failure['expected_subject']} | "
                f"top1={failure.get('top1_subject')} | "
                f"top3={failure.get('top3_subjects')} | "
                f"query={failure['query']}"
            )

    print()
    print("Failure count by expected subject:")

    if failures:
        counts = Counter(
            failure["expected_subject"]
            for failure in failures
        )

        for subject, count in counts.most_common():
            print(f"  {count:2}  {subject}")
    else:
        print("  None")

    output_path = RESULTS_DIR / "retrieval_results.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            results,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print(f"Detailed results: {output_path}")


if __name__ == "__main__":
    main()
