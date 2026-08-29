from __future__ import annotations

from pathlib import Path


SAMPLES_DIR = Path(
    "evaluation/ingestion/results/metadata_samples"
)


KEYWORDS = (
    "course",
    "credit",
    "hour",
    "semester",
    "programme",
    "program",
    "subject",
    "title",
)


def main() -> None:
    files = sorted(
        SAMPLES_DIR.glob("*.md")
    )

    for path in files:
        text = path.read_text(
            encoding="utf-8"
        )

        lines = text.splitlines()

        relevant = []

        for index, line in enumerate(lines):
            normalized = line.lower()

            if any(
                keyword in normalized
                for keyword in KEYWORDS
            ):
                relevant.append(
                    (index + 1, line.strip())
                )

        print()
        print("=" * 100)
        print(path.name)
        print("=" * 100)

        for line_number, line in relevant[:80]:
            print(
                f"{line_number:4}: {line}"
            )


if __name__ == "__main__":
    main()
