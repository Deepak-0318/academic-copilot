from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class QueryIntent:
    name: str
    preferred_section: str | None


INTENT_RULES: list[tuple[str, str, list[str]]] = [
    (
        "assessment_query",
        "assessment",
        [
            "assessment",
            "assessments",
            "exam",
            "exams",
            "cie",
            "see",
            "weightage",
            "marks",
        ],
    ),
    (
        "co_po_query",
        "co_po_mapping",
        [
            "co-po",
            "co po",
            "program outcome",
            "program outcomes",
            "po1",
            "po2",
            "po3",
            "po4",
            "po5",
            "po6",
            "po7",
            "po8",
            "po9",
            "po10",
            "po11",
            "po12",
            "course outcome",
            "course outcomes",
            "co1",
            "co2",
            "co3",
            "co4",
            "co5",
            "co6",
        ],
    ),
    (
        "course_objectives_query",
        "course_objectives",
        [
            "objective",
            "objectives",
        ],
    ),
    (
        "reference_query",
        "references",
        [
            "textbook",
            "textbooks",
            "reference book",
            "reference books",
            "references",
            "online reference",
            "online references",
        ],
    ),
    (
        "lab_query",
        "lab_programs",
        [
            "lab",
            "laboratory",
            "experiment",
            "experiments",
        ],
    ),
    (
        "lesson_plan_query",
        "lesson_plan",
        [
            "lesson plan",
            "teaching method",
            "learning objective",
            "bloom",
        ],
    ),
    (
        "syllabus_query",
        "syllabus",
        [
            "syllabus",
            "module",
            "modules",
            "unit",
            "units",
            "topics covered",
        ],
    ),
    (
        "course_metadata_query",
        "course_metadata",
        [
            "course code",
            "coursecode",
            "semester",
            "credits",
            "credit",
            "hours per week",
            "teaching hours",
            "total teaching hours",
        ],
    ),
]

def classify_query(query: str) -> QueryIntent:
    if not query.strip():
        raise ValueError("Query cannot be empty.")

    normalized = " ".join(
        query.lower().strip().split()
    )

    for intent_name, section, keywords in INTENT_RULES:
        for keyword in keywords:
            pattern = rf"\b{re.escape(keyword.lower())}\b"

            if re.search(pattern, normalized):
                return QueryIntent(
                    name=intent_name,
                    preferred_section=section,
                )

    return QueryIntent(
        name="general_academic_query",
        preferred_section=None,
    )