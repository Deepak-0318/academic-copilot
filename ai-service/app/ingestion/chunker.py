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
        r"^\s*(?:#+\s*)?\|?\s*"
        r"(?:Reference\s+books?|References?|Text\s+books?)"
        r"\b.*$",
    ),

    (
        "lab_programs",
        r"^\s*(?:#+\s*)?\|?\s*"
        r"(?:Lab\s+Programs?|Lab\s+Activities|Lab\s+Practicals|"
        r"Laboratory\s+Components?|Experiment\s+\d+)"
        r"\b.*$",
    ),

    (
        "lesson_plan",
        r"^\s*(?:#+\s*)?\|?\s*"
        r"(?:Lesson\s+plan|Teaching\s+plan|Session\s*\|"
        r"\s*Module\s+No\.\s*\|\s*Topic)"
        r"\b.*$",
    ),

    (
        "assessment",
        r"^\s*(?:#+\s*)?"
        r"(?:Assessment\s+and\s+Evaluation|Assessment\s+Plan|"
        r"Evaluation\s+of\s+Components|Rubrics)"
        r"\b.*$",
    ),

    (
        "co_po_mapping",
        r"^(?:#+\s*)?Course\s+Outcomes-\s*Programme\s+Outcomes\s+Matrix",
    ),

    (
        "course_outcomes",
        r"^\s*(?:#+\s*)?\|?\s*Course\s+Outcomes?\b.*$",
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


def is_table_line(line: str) -> bool:
    return line.strip().startswith("|")


def is_heading_line(line: str) -> bool:
    return re.match(r"^\s*#{1,6}\s+\S", line) is not None


def first_heading(content: str) -> str | None:
    for line in content.splitlines():
        stripped = line.strip()

        if is_heading_line(stripped):
            return stripped

    return None


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


def split_into_blocks(content: str) -> list[str]:
    """Split text into paragraphs, headings, and whole Markdown tables."""

    blocks: list[str] = []
    current: list[str] = []
    in_table = False

    def flush_current() -> None:
        nonlocal current

        block = "\n".join(current).strip()

        if block:
            blocks.append(block)

        current = []

    for line in content.splitlines():
        stripped = line.strip()

        if is_table_line(line):
            if current and not in_table:
                flush_current()

            current.append(line)
            in_table = True
            continue

        if in_table:
            flush_current()
            in_table = False

        if not stripped:
            flush_current()
            continue

        if is_heading_line(line):
            flush_current()
            current.append(line)
            flush_current()
            continue

        current.append(line)

    flush_current()

    return blocks


def split_text_block(
    block: str,
    max_characters: int,
    overlap_characters: int,
) -> list[str]:
    if len(block) <= max_characters:
        return [block]

    lines = block.splitlines()
    pieces: list[str] = []
    current: list[str] = []

    for line in lines:
        candidate = "\n".join([*current, line]).strip()

        if len(candidate) <= max_characters:
            current.append(line)
            continue

        if current:
            pieces.append("\n".join(current).strip())
            current = []

        if len(line) <= max_characters:
            current.append(line)
            continue

        start = 0

        while start < len(line):
            end = start + max_characters
            piece = line[start:end].strip()

            if piece:
                pieces.append(piece)

            if end >= len(line):
                break

            start = max(
                end - overlap_characters,
                start + 1,
            )

    if current:
        pieces.append("\n".join(current).strip())

    return pieces


def split_table_block(
    block: str,
    max_characters: int,
) -> list[str]:
    if len(block) <= max_characters:
        return [block]

    rows = [
        line
        for line in block.splitlines()
        if line.strip()
    ]

    if not rows:
        return []

    separator_pattern = r"\|\s*:?-{3,}:?\s*\|"
    header = rows[:1]

    if len(rows) > 1 and re.search(separator_pattern, rows[1]):
        header = rows[:2]

    body = rows[len(header):]
    chunks: list[str] = []
    current = header.copy()
    header_text = "\n".join(header).strip()

    for row in body:
        candidate = "\n".join([*current, row])

        if len(candidate) <= max_characters:
            current.append(row)
            continue

        if len(current) > len(header):
            chunks.append("\n".join(current).strip())
            current = header.copy()

        if len("\n".join([*header, row])) <= max_characters:
            current.append(row)
            continue

        available_characters = max(
            max_characters - len(header_text) - 2,
            max_characters // 2,
        )

        for piece in split_text_block(
            row,
            available_characters,
            overlap_characters=0,
        ):
            contextualized_piece = (
                f"{header_text}\n{piece}"
                if header_text
                else piece
            )

            chunks.append(contextualized_piece.strip())

    if len(current) > len(header):
        chunks.append("\n".join(current).strip())

    return chunks or [block[:max_characters].strip()]


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

    blocks = split_into_blocks(content)

    chunks: list[str] = []
    current = ""
    context_heading = first_heading(content)

    for block in blocks:
        block = block.strip()

        if not block:
            continue

        oversized_pieces = (
            split_table_block(block, max_characters)
            if is_table_line(block)
            else split_text_block(
                block,
                max_characters,
                overlap_characters,
            )
        )

        for piece in oversized_pieces:
            candidate = (
                piece
                if not current
                else f"{current}\n\n{piece}"
            )

            if len(candidate) <= max_characters:
                current = candidate
                continue

            if current:
                chunks.append(current)

            current = piece

    if current:
        chunks.append(current)

    if not context_heading:
        return chunks

    contextualized: list[str] = []

    for index, chunk in enumerate(chunks):
        if index == 0 or context_heading in chunk:
            contextualized.append(chunk)
            continue

        prefixed = f"{context_heading}\n\n{chunk}"

        if len(prefixed) <= max_characters:
            contextualized.append(prefixed)
        else:
            contextualized.append(chunk)

    return contextualized


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
