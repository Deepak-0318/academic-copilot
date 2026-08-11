from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class AcademicChunk:
    content: str
    section: str
    chunk_index: int
    metadata: dict = field(default_factory=dict)


# These are the academic sections we want to preserve.
SECTION_PATTERNS = [
    (
        "course_objectives",
        r"^\s*\|?\s*Course\s+Objectives\s*:?.*$",
    ),

    (
        "syllabus",
        r"^\s*(?:#+\s*)?\|?\s*"
        r"(?:Course\s+outline\s*\(Syllabus\s+of\s+the\s+course\)|Syllabus)"
        r"\s*:?.*$",
    ),

    (
        "references",
        r"^\s*\|?\s*Reference\s+books\s*\|",
    ),

    (
        "lab_programs",
        r"^(?:#+\s*)?Lab\s+Programs(?:\s*\[\d+\s*Hrs?\])?",
    ),

    (
        "lesson_plan",
        r"^\s*\|?\s*Session\s*\|\s*Module\s+No\.\s*\|\s*Topic",
    ),

    (
        "assessment",
        r"^#+\s*Assessment\s+and\s+Evaluation",
    ),

    (
        "co_po_mapping",
        r"^(?:#+\s*)?Course\s+Outcomes-\s*Programme\s+Outcomes\s+Matrix",
    ),

    (
        "course_outcomes",
        r"^#+\s*Course\s+Outcomes?\s*$",
    ),
]

def normalize_text(text: str) -> str:
    """Normalize whitespace while preserving line structure."""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove Docling image placeholders.
    text = re.sub(r"<!--\s*image\s*-->", "", text, flags=re.IGNORECASE)

    # Normalize excessive spaces.
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def detect_section(line: str) -> str | None:
    """Return the academic section represented by a line."""

    for section, pattern in SECTION_PATTERNS:
        if re.search(pattern, line, flags=re.IGNORECASE):
            return section

    return None


def split_into_sections(markdown: str) -> list[tuple[str, str]]:
    """
    Split document markdown into logical academic sections.

    Returns:
        List of (section_name, section_content)
    """

    lines = markdown.splitlines()

    sections: list[tuple[str, str]] = []

    current_section = "course_metadata"
    current_lines: list[str] = []

    for line in lines:
        detected = detect_section(line)

        if detected is not None and detected != current_section and current_lines:
            content = "\n".join(current_lines).strip()

            if content:
                sections.append((current_section, content))

            current_section = detected
            current_lines = [line]
        else:
            current_lines.append(line)

    # Flush final section.
    content = "\n".join(current_lines).strip()

    if content:
        sections.append((current_section, content))

    return sections


def split_large_section(
    content: str,
    max_characters: int = 3000,
    overlap_characters: int = 300,
) -> list[str]:
    """
    Split a large academic section while attempting to preserve paragraphs
    and table boundaries.

    We use character limits only as a safety mechanism after semantic
    section detection.
    """

    if len(content) <= max_characters:
        return [content]

    paragraphs = re.split(r"\n\s*\n", content)

    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        candidate = (
            paragraph
            if not current
            else f"{current}\n\n{paragraph}"
        )

        if len(candidate) <= max_characters:
            current = candidate
            continue

        if current:
            chunks.append(current)

        # Handle a single oversized paragraph/table.
        if len(paragraph) > max_characters:
            start = 0

            while start < len(paragraph):
                end = start + max_characters
                piece = paragraph[start:end]

                if piece.strip():
                    chunks.append(piece.strip())

                start = max(
                    end - overlap_characters,
                    start + 1,
                )

            current = ""
        else:
            current = paragraph

    if current:
        chunks.append(current)

    return chunks


def create_chunks(
    markdown: str,
    *,
    subject: str,
    document_id: str | None = None,
    course_code: str | None = None,
    university: str | None = None,
    regulation: str | None = None,
    branch: str | None = None,
    semester: int | None = None,
    max_characters: int = 3000,
    overlap_characters: int = 300,
    min_characters: int = 200,
) -> list[AcademicChunk]:
    """
    Convert Docling Markdown into academic-aware RAG chunks.
    """

    markdown = normalize_text(markdown)

    sections = split_into_sections(markdown)

    chunks: list[AcademicChunk] = []

    chunk_index = 0

    base_metadata = {
        "subject": subject,
        "course_code": course_code,
        "university": university,
        "regulation": regulation,
        "branch": branch,
        "semester": semester,
    }

    if document_id is not None:
        base_metadata["document_id"] = document_id

    for section_name, section_content in sections:
        section_chunks = split_large_section(
            section_content,
            max_characters=max_characters,
            overlap_characters=overlap_characters,
        )

        for section_chunk in section_chunks:
            section_chunk = section_chunk.strip()
            
            if len(section_chunk) < min_characters:
                continue
            
            metadata = {
                **base_metadata,
                "section": section_name,
            }
            
            chunks.append(
                AcademicChunk(
                    content=section_chunk,
                    section=section_name,
                    chunk_index=chunk_index,
                    metadata=metadata,
                )
            )
            
            chunk_index += 1

    return chunks