from __future__ import annotations

import json
from pathlib import Path


RESULTS_FILE = Path(
    "evaluation/ingestion/results/metadata_corpus.json"
)


def main() -> None:
    results = json.loads(
        RESULTS_FILE.read_text(encoding="utf-8")
    )

    fields = [
        "subject",
        "course_code",
        "programme",
        "semester",
        "credits",
        "teaching_hours",
    ]

    for field in fields:
        missing = [
            item
            for item in results
            if item.get(field) is None
        ]

        print()
        print("=" * 80)
        print(
            f"MISSING: {field} "
            f"({len(missing)}/{len(results)})"
        )
        print("=" * 80)

        for item in missing:
            print(
                f"{item['subject_folder']}"
                f" | {item['file']}"
            )


if __name__ == "__main__":
    main()
