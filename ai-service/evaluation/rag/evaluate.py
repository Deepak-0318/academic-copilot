from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any

from app.retrieval.service import AcademicRetrievalService


BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_FILE = BASE_DIR / "questions.json"
RESULTS_DIR = BASE_DIR / "results"
BASELINE_FILE = RESULTS_DIR / "baseline.json"

TOP_K = 5


def load_questions() -> list[dict[str, Any]]:
    with QUESTIONS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def is_relevant(
    result: dict[str, Any],
    question: dict[str, Any],
) -> bool:
    expected_sections = set(
        question.get("expected_sections", [])
    )

    result_section = result.get("section")

    if result_section not in expected_sections:
        return False

    expected_subject = question.get(
        "expected_subject"
    )

    if expected_subject:
        metadata = result.get("metadata") or {}

        result_subject = metadata.get("subject")

        if (
            result_subject
            and result_subject != expected_subject
        ):
            return False

    expected_course_code = question.get(
        "expected_course_code"
    )

    if expected_course_code:
        metadata = result.get("metadata") or {}

        result_course_code = metadata.get(
            "course_code"
        )

        if (
            result_course_code
            and result_course_code != expected_course_code
        ):
            return False

    return True


def reciprocal_rank(
    results: list[dict[str, Any]],
    question: dict[str, Any],
) -> float:
    for rank, result in enumerate(
        results,
        start=1,
    ):
        if is_relevant(result, question):
            return 1.0 / rank

    return 0.0


def recall_at_k(
    results: list[dict[str, Any]],
    question: dict[str, Any],
    k: int,
) -> float:
    top_results = results[:k]

    for result in top_results:
        if is_relevant(result, question):
            return 1.0

    return 0.0


def evaluate_question(
    retrieval_service: AcademicRetrievalService,
    question: dict[str, Any],
) -> dict[str, Any]:

    results = retrieval_service.search(
        question["question"],
        limit=TOP_K,
        subject=question.get("expected_subject"),
        course_code=question.get("expected_course_code"),
    )

    return {
        "id": question["id"],
        "question": question["question"],
        "expected_sections": question[
            "expected_sections"
        ],
        "retrieved": [
            {
                "rank": rank,
                "section": result.get("section"),
                "similarity": result.get("similarity"),
                "chunk_id": result.get("chunk_id"),
                "document_id": result.get(
                    "document_id"
                ),
            }
            for rank, result in enumerate(
                results,
                start=1,
            )
        ],
        "recall_at_1": recall_at_k(
            results,
            question,
            1,
        ),
        "recall_at_3": recall_at_k(
            results,
            question,
            3,
        ),
        "recall_at_5": recall_at_k(
            results,
            question,
            5,
        ),
        "reciprocal_rank": reciprocal_rank(
            results,
            question,
        ),
    }


def calculate_metrics(
    evaluations: list[dict[str, Any]],
) -> dict[str, float]:

    return {
        "recall_at_1": mean(
            item["recall_at_1"]
            for item in evaluations
        ),
        "recall_at_3": mean(
            item["recall_at_3"]
            for item in evaluations
        ),
        "recall_at_5": mean(
            item["recall_at_5"]
            for item in evaluations
        ),
        "mrr": mean(
            item["reciprocal_rank"]
            for item in evaluations
        ),
    }


def main() -> None:
    questions = load_questions()

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    retrieval_service = AcademicRetrievalService()

    evaluations: list[dict[str, Any]] = []

    for index, question in enumerate(
        questions,
        start=1,
    ):
        print(
            f"[{index}/{len(questions)}] "
            f"{question['id']}: "
            f"{question['question']}"
        )

        evaluation = evaluate_question(
            retrieval_service,
            question,
        )

        evaluations.append(evaluation)

    metrics = calculate_metrics(
        evaluations
    )

    output = {
        "benchmark": {
            "question_count": len(questions),
            "top_k": TOP_K,
        },
        "metrics": metrics,
        "questions": evaluations,
    }

    with BASELINE_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            output,
            file,
            indent=2,
        )

    print()
    print("RAG Evaluation Complete")
    print("-----------------------")
    print(
        f"Recall@1 : "
        f"{metrics['recall_at_1']:.4f}"
    )
    print(
        f"Recall@3 : "
        f"{metrics['recall_at_3']:.4f}"
    )
    print(
        f"Recall@5 : "
        f"{metrics['recall_at_5']:.4f}"
    )
    print(
        f"MRR      : "
        f"{metrics['mrr']:.4f}"
    )
    print()
    print(
        f"Results saved to: "
        f"{BASELINE_FILE}"
    )


if __name__ == "__main__":
    main()