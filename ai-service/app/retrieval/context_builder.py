from __future__ import annotations

from typing import Any


def build_context(
    results: list[dict[str, Any]],
) -> str:
    """
    Build deterministic LLM context from retrieved chunks.

    Results are expected to be ordered by retrieval relevance.
    """

    if not results:
        return ""

    sections: list[str] = []

    for index, result in enumerate(results, start=1):
        section = result.get("section") or "unknown"
        content = (result.get("content") or "").strip()

        if not content:
            continue

        sections.append(
            f"[SOURCE {index}]\n"
            f"Section: {section}\n"
            f"Similarity: {result.get('similarity', 0.0):.4f}\n"
            f"Content:\n{content}"
        )

    return "\n\n".join(sections)