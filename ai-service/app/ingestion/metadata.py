from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class AcademicMetadata:
    subject: str | None = None
    course_code: str | None = None
    programme: str | None = None
    semester: int | None = None
    credits: int | None = None
    teaching_hours: int | None = None


ROMAN_SEMESTERS = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
}


METADATA_LABELS = [
    "Course Code",
    "Course Title",
    "Name of the Course",
    "Course Name",
    "Title of the Course",
    "Subject",
    "Subject Name",
    "Name of the Programme",
    "Programme",
    "Program",
    "Name of Program",
    "Semester",
    "Course Credit",
    "Course Credits",
    "Credits",
    "Credits L:T:P Hours",
    "Total Hours",
    "Total no. of Teaching hours",
    "TotalNo. of Teaching Hours",
    "Teaching Hours",
]


GENERIC_TITLE_TOKENS = {
    "assessmentandevaluation",
    "cie1mcq",
    "cie1presentation",
    "cie2midtermexamination",
    "courseobjectives",
    "courseoutcomes",
    "courseoutline",
    "courseoutlinesyllabusofthecourse",
    "courseoutlinesyllabusofthecoursetemplate1",
    "courseoutcomesprogrammeoutcomesmatrix",
    "index",
    "indexsheetforcoursefile",
    "lessonplan",
    "lessonplantemplate2",
    "references",
    "referencebooks",
    "rubrics",
    "rubricsforevaluationofcie",
    "syllabus",
    "tableofcontents",
    "textbooks",
}


def _clean(value: str | None) -> str | None:
    if not value:
        return None

    value = re.sub(r"\s+", " ", value)
    value = value.strip(" |:")

    if not value:
        return None

    value = re.sub(r"^-+$", "", value).strip()

    return value or None


def _normalize_header(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _strip_markdown_heading(value: str) -> str:
    value = value.strip()
    value = re.sub(r"^#{1,6}\s*", "", value)
    value = value.strip(" |:")
    return value


def _is_metadata_label(value: str) -> bool:
    normalized = _normalize_header(
        _strip_markdown_heading(value)
    )

    label_tokens = {
        _normalize_header(label)
        for label in METADATA_LABELS
    }

    return normalized in label_tokens


def _label_pattern(labels: list[str]) -> str:
    return "|".join(
        re.escape(label)
        for label in sorted(
            labels,
            key=len,
            reverse=True,
        )
    )


def _is_generic_title(value: str) -> bool:
    value = _strip_markdown_heading(value)
    normalized = _normalize_header(value)

    if not normalized:
        return True

    if normalized in GENERIC_TITLE_TOKENS:
        return True

    if re.search(
        r"\b(?:module|unit|session|table|cie|see|co|po)\b",
        value,
        flags=re.IGNORECASE,
    ):
        return True

    if re.search(
        r"\b(?:contents?|syllabus|references?|rubrics?|"
        r"assessment|objectives?|outcomes?|lesson\s+plan|"
        r"course\s+outline|text\s*books?)\b",
        value,
        flags=re.IGNORECASE,
    ):
        return True

    if re.search(
        r"\b(?:rvu\.edu|vidyaniketan|educational\s+institutions|"
        r"bengaluru|mysuru|india|phone|www\.)\b",
        value,
        flags=re.IGNORECASE,
    ):
        return True

    return False


def _clean_title_candidate(
    value: str | None,
    *,
    require_alpha: bool = True,
) -> str | None:
    value = _clean(value)

    if not value:
        return None

    value = _strip_markdown_heading(value)
    value = re.sub(r"\s*#+\s*$", "", value)
    value = re.sub(r"\s+\(\s*$", "", value)
    value = _clean(value)

    if not value:
        return None

    if _is_metadata_label(value):
        return None

    if _is_generic_title(value):
        return None

    if len(value) > 120:
        return None

    if require_alpha and not re.search(r"[A-Za-z]", value):
        return None

    return value


def _table_rows(markdown: str) -> list[list[str]]:
    """
    Return meaningful Markdown table rows while preserving
    empty-cell positions.

    Preserving empty cells is important because Docling may split
    table headers across multiple rows, for example:

        | Course credit | No. of hours per week | Total no. of Teaching |
        |               | (L + T + P)           | hours                  |
        | 3             | 2+0+2                 | 60                     |
    """

    rows: list[list[str]] = []

    for line in markdown.splitlines():
        stripped = line.strip()

        if not stripped.startswith("|"):
            continue

        cells = [
            cell.strip()
            for cell in stripped.strip("|").split("|")
        ]

        # Ignore completely empty rows.
        if not any(cells):
            continue

        # Ignore Markdown separator rows.
        non_empty_cells = [
            cell
            for cell in cells
            if cell
        ]

        if non_empty_cells and all(
            re.fullmatch(r":?-+:?", cell)
            for cell in non_empty_cells
        ):
            continue

        # IMPORTANT:
        # Do NOT remove empty cells here.
        # Their positions represent the original table columns.
        rows.append(cells)

    return rows

def _value_from_table_row(
    markdown: str,
    labels: list[str],
) -> str | None:
    normalized_labels = {
        _normalize_header(label)
        for label in labels
    }

    for cells in _table_rows(markdown):
        for index, cell in enumerate(cells):
            normalized_cell = _normalize_header(cell)

            if normalized_cell not in normalized_labels:
                for label in sorted(
                    labels,
                    key=len,
                    reverse=True,
                ):
                    label_pattern = re.escape(label)
                    match = re.match(
                        rf"^\s*(?:#+\s*)?{label_pattern}"
                        rf"\s*(?::|\|)?\s*(?P<value>.+)$",
                        cell,
                        flags=re.IGNORECASE,
                    )

                    if not match:
                        continue

                    value = _clean(match.group("value"))

                    if value:
                        return value

                continue

            for next_index in range(index + 1, len(cells)):
                value = _clean(cells[next_index])

                if not value:
                    continue

                if value in {":", "-", "—"}:
                    continue

                return value

    return None


def _value_from_labeled_line(
    markdown: str,
    labels: list[str],
) -> str | None:
    label_pattern = _label_pattern(labels)

    pattern = re.compile(
        rf"^\s*(?:#+\s*)?(?:{label_pattern})"
        rf"\s*(?::|\|)?\s*"
        rf"(?P<value>.*?)"
        rf"\s*$",
        flags=re.IGNORECASE,
    )

    lines = markdown.splitlines()

    for index, line in enumerate(lines):
        match = pattern.match(line)

        if not match:
            continue

        value = _clean(match.group("value"))

        if value:
            value = re.sub(
                rf"^(?:{label_pattern})\s*(?::|\|)?\s*",
                "",
                value,
                flags=re.IGNORECASE,
            )

            value = _clean(value)

            if value:
                return value

        for next_line in lines[index + 1:index + 5]:
            candidate = _clean_title_candidate(
                next_line,
                require_alpha=False,
            )

            if not candidate:
                if _is_metadata_label(next_line):
                    break

                continue

            return candidate

    return None


def _extract_subject_from_heading(markdown: str) -> str | None:
    """
    Use only early, meaningful document headings as a subject fallback.

    This intentionally skips structural headings such as Lesson plan,
    Syllabus, References, Course Objectives, modules, tables, and
    assessment sections.
    """

    lines = markdown.splitlines()

    for line in lines[:80]:
        stripped = line.strip()

        if not stripped:
            continue

        if re.match(
            r"^\s*(?:#+\s*)?(?:course\s+objectives?|"
            r"course\s+outcomes?|syllabus|module|unit|"
            r"assessment|references?)\b",
            stripped,
            flags=re.IGNORECASE,
        ):
            break

        if not re.match(r"^\s*#{1,6}\s+", stripped):
            continue

        candidate = _clean_title_candidate(stripped)

        if candidate:
            return candidate

    return None


def _extract_subject_from_category_cell(markdown: str) -> str | None:
    """
    Extract subject from table cells of the form:

        <Course Name> Category: <category description>

    Some RV Vidyaniketan documents (e.g. English Communication) embed
    the course name directly in a metadata table cell followed by
    "Category:".  No standard label row ("Course Title:", etc.) is
    present, so the ordinary label-based extractors find nothing.

    This function scans only the first 30 lines of the document for
    such cells and returns the text preceding "Category:" after
    passing it through _clean_title_candidate to reject generic or
    institution-level strings.
    """

    # Only inspect the preamble — the subject table always appears
    # within the first page (first 30 lines of Docling output).
    preamble = "\n".join(markdown.splitlines()[:30])

    for cells in _table_rows(preamble):
        for cell in cells:
            match = re.match(
                r"^(?P<name>.+?)\s+Category\s*:.*$",
                cell.strip(),
                flags=re.IGNORECASE,
            )

            if not match:
                continue

            candidate = _clean_title_candidate(match.group("name"))

            if candidate:
                return candidate

    return None


def _value_from_inline_text(
    markdown: str,
    labels: list[str],
) -> str | None:
    label_pattern = _label_pattern(labels)

    all_labels = METADATA_LABELS

    stop_pattern = _label_pattern(
        [
            label
            for label in all_labels
            if label not in labels
        ]
    )

    pattern = re.compile(
        rf"(?:{label_pattern})"
        rf"\s*:?\s*\|?\s*:?\s*"
        rf"(?P<value>[^|\n]+?)"
        rf"(?=\s*(?:#+\s*)?(?:{stop_pattern})\b|\s*\||$)",
        flags=re.IGNORECASE,
    )

    for match in pattern.finditer(markdown):
        value = _clean(match.group("value"))

        if value:
            return value

    return None


def _extract_course_code(markdown: str) -> str | None:
    value = _value_from_table_row(
        markdown,
        [
            "Course Code",
            "Course code",
        ],
    )

    if value:
        match = re.search(
            r"\b[A-Za-z]{2,}\d{3,}\b",
            value,
        )

        if match:
            return match.group()

    value = _value_from_labeled_line(
        markdown,
        [
            "Course Code",
            "Course code",
        ],
    )

    if value:
        match = re.search(
            r"\b[A-Za-z]{2,}\d{3,}\b",
            value,
        )

        if match:
            return match.group()

    match = re.search(
        r"\bCourse\s+Code\s*:?\s*"
        r"([A-Za-z]{2,}\d{3,})\b",
        markdown,
        flags=re.IGNORECASE,
    )

    if match:
        return match.group(1)

    # Some course documents place the code near the beginning
    # without the explicit "Course Code" label.
    match = re.search(
        r"\b([A-Z]{2,}[A-Z0-9]{0,4}\d{3,})\b",
        markdown,
    )

    return match.group(1) if match else None


def _extract_subject(markdown: str) -> str | None:
    labels = [
        "Name of the Course",
        "Course Title",
        "Course Name",
        "Title of the Course",
        "Subject",
        "Subject Name",
    ]

    value = _value_from_table_row(markdown, labels)

    if value:
        return _clean_subject(value)

    value = _value_from_labeled_line(markdown, labels)

    if value:
        return _clean_subject(value)

    value = _value_from_inline_text(markdown, labels)

    if value:
        return _clean_subject(value)

    value = _extract_subject_from_category_cell(markdown)

    if value:
        return _clean_subject(value)

    value = _extract_subject_from_heading(markdown)

    return _clean_subject(value)


def _extract_programme(markdown: str) -> str | None:
    labels = [
        "Name of the Programme",
        "Programme",
        "Program",
        "Name of Program",
        "Degree Programme",
        "Degree Program",
    ]

    value = _value_from_table_row(markdown, labels)

    if value:
        return value

    value = _value_from_labeled_line(markdown, labels)

    if value:
        return value

    value = _value_from_inline_text(markdown, labels)

    if value:
        return value

    # Common heading-style forms:
    #
    # B.Tech (Hons.) CSE
    # BTech (H)
    # BCA
    #
    # Only use this fallback when an explicit programme-like
    # academic phrase is present.
    programme_patterns = [
        r"\bB\.?\s*Tech(?:nology)?\s*\([^)\n]+\)\s*[A-Za-z &/-]*",
        r"\bBTech\s*\([^)\n]+\)\s*[A-Za-z &/-]*",
        r"\bBCA\b",
        r"\bB\.?\s*Tech\b",
        r"\bM\.?\s*Tech\b",
    ]

    for pattern in programme_patterns:
        match = re.search(
            pattern,
            markdown,
            flags=re.IGNORECASE,
        )

        if match:
            value = _clean(match.group())

            if value:
                return value

    return None

def _parse_semester(value: str | None) -> int | None:
    if not value:
        return None

    value = value.upper().strip()

    match = re.search(
        r"\b(VIII|VII|VI|IV|III|II|I|\d{1,2})\b",
        value,
    )

    if not match:
        return None

    token = match.group(1)

    if token in ROMAN_SEMESTERS:
        return ROMAN_SEMESTERS[token]

    number = int(token)

    if 1 <= number <= 12:
        return number

    return None


def _extract_semester(markdown: str) -> int | None:
    value = _value_from_table_row(
        markdown,
        ["Semester"],
    )

    if value:
        semester = _parse_semester(value)

        if semester:
            return semester

    value = _value_from_labeled_line(
        markdown,
        ["Semester"],
    )

    if value:
        semester = _parse_semester(value)

        if semester:
            return semester

    match = re.search(
        r"\bSemester\s*:?\s*"
        r"(VIII|VII|VI|IV|III|II|I|\d{1,2})\b",
        markdown,
        flags=re.IGNORECASE,
    )

    if match:
        return _parse_semester(match.group(1))

    return None


def _extract_number_after_label(
    markdown: str,
    labels: list[str],
) -> int | None:
    label_pattern = _label_pattern(labels)

    pattern = re.compile(
        rf"\b(?:{label_pattern})\b"
        rf"\s*(?::|\|)?\s*"
        rf"(?:\|?\s*:?\s*)?"
        rf"(?P<value>\d+)",
        flags=re.IGNORECASE,
    )

    for match in pattern.finditer(markdown):
        return int(match.group("value"))

    return None


def _find_numeric_table_value(
    rows: list[list[str]],
    header_tokens: set[str],
    *,
    max_lookahead: int = 4,
) -> int | None:
    """
    Find a numeric value belonging to a table column.

    Handles Docling tables where the header spans multiple
    Markdown rows, e.g.:

        | Course credit | No. of hours per week | Total no. of Teaching |
        |                | (L + T + P)          | hours                 |
        | 3              | 2+0+2                | 60                    |

    The important part is that the actual value may not be
    immediately on the next Markdown row.
    """

    for index, row in enumerate(rows):
        normalized = [
            _normalize_header(cell)
            for cell in row
        ]

        column_indexes = [
            i
            for i, cell in enumerate(normalized)
            if cell in header_tokens
            or any(
                token in cell
                for token in header_tokens
            )
        ]

        if not column_indexes:
            continue

        for column_index in column_indexes:
            for offset in range(1, max_lookahead + 1):
                next_index = index + offset

                if next_index >= len(rows):
                    break

                value_row = rows[next_index]

                if column_index >= len(value_row):
                    continue

                value = _clean(value_row[column_index])

                if not value:
                    continue

                # Ignore Markdown/header continuation rows.
                if _normalize_header(value) in {
                    "hours",
                    "ltp",
                    "ltp",
                }:
                    continue

                match = re.search(
                    r"\b(\d+)\b",
                    value,
                )

                if match:
                    return int(match.group(1))

    return None


def _extract_credits(markdown: str) -> int | None:
    """
    Extract course credits.

    Supports:
    - normal metadata tables
    - split/multiline Docling table headers
    - labelled lines
    - inline metadata
    """

    rows = _table_rows(markdown)

    # Standard and split-header table formats.
    value = _find_numeric_table_value(
        rows,
        {
            "coursecredit",
            "coursecredits",
            "credits",
            "credit",
        },
    )

    if value is not None:
        return value

    # Engineering Explorations-style:
    # | Credits L:T:P Hours | 3 | 2+0+4 | 60 |
    value = _value_from_table_row(
        markdown,
        [
            "Credits L:T:P Hours",
            "Credits L:T:P",
        ],
    )

    if value:
        match = re.search(
            r"\b(\d+)\b",
            value,
        )

        if match:
            return int(match.group(1))

    # Labelled-line formats.
    value = _value_from_labeled_line(
        markdown,
        [
            "Course Credit",
            "Course Credits",
            "Credits",
            "Credit",
        ],
    )

    if value:
        match = re.search(
            r"\b(\d+)\b",
            value,
        )

        if match:
            return int(match.group(1))

    value = _value_from_inline_text(
        markdown,
        [
            "Course Credit",
            "Course Credits",
            "Credits",
            "Credit",
        ],
    )

    if value:
        match = re.search(
            r"\b(\d+)\b",
            value,
        )

        if match:
            return int(match.group(1))

    return None


def _parse_total_hours(value: str) -> int | None:
    if not value:
        return None

    value = value.strip()

    match = re.fullmatch(
        r"\s*(\d+)\s*(?:hours?)?\s*",
        value,
        flags=re.IGNORECASE,
    )

    if match:
        hours = int(match.group(1))

        if 0 < hours <= 1000:
            return hours

    # Examples:
    # 30L+30P
    # 30 L + 30 P
    # 30L + 30P + 15T
    components = re.findall(
        r"(\d+)\s*([LTP])\b",
        value,
        flags=re.IGNORECASE,
    )

    if components:
        total = sum(
            int(number)
            for number, _kind in components
        )

        if 0 < total <= 1000:
            return total

    # Fallback for expressions such as:
    # 30 + 30
    numbers = re.findall(r"\b\d+\b", value)

    if len(numbers) >= 2:
        total = sum(int(number) for number in numbers)

        if 0 < total <= 1000:
            return total

    match = re.search(r"\d+", value)

    if match:
        hours = int(match.group())

        if 0 < hours <= 1000:
            return hours

    return None


def _extract_teaching_hours(markdown: str) -> int | None:
    """Extract total teaching hours from academic metadata tables."""

    rows = _table_rows(markdown)

    # ---------------------------------------------------------
    # 1. Standard single-row metadata table
    # ---------------------------------------------------------
    for index, row in enumerate(rows):
        normalized = [
            _normalize_header(cell)
            for cell in row
        ]

        teaching_index = None

        for i, cell in enumerate(normalized):
            if "teachinghours" in cell:
                teaching_index = i
                break

        if teaching_index is None:
            continue

        if index + 1 < len(rows):
            value_row = rows[index + 1]

            if teaching_index < len(value_row):
                value = value_row[teaching_index]

                match = re.search(r"\b(\d+)\b", value)

                if match:
                    return int(match.group(1))

    # ---------------------------------------------------------
    # 2. Split/multi-row table header
    #
    # Example:
    #
    # | Course credit | No. of hours per week | Total no. of Teaching |
    # |               | (L + T + P)           | hours                  |
    # | 3             | 2+0+2                 | 60                     |
    # ---------------------------------------------------------
    for header_index in range(len(rows) - 1):
        header = rows[header_index]
        next_row = rows[header_index + 1]

        header_normalized = [
            _normalize_header(cell)
            for cell in header
        ]

        next_normalized = [
            _normalize_header(cell)
            for cell in next_row
        ]

        for column_index, cell in enumerate(header_normalized):
            if "teaching" not in cell:
                continue

            # The second header row should contain "hours".
            continuation = (
                next_normalized[column_index]
                if column_index < len(next_normalized)
                else ""
            )

            if "hour" not in continuation:
                continue

            # The actual data row follows the two header rows.
            data_index = header_index + 2

            if data_index >= len(rows):
                continue

            data_row = rows[data_index]

            if column_index >= len(data_row):
                continue

            value = data_row[column_index]

            match = re.search(r"\b(\d+)\b", value)

            if match:
                return int(match.group(1))

    # ---------------------------------------------------------
    # 3. Alternative Total Hours format
    #
    # | Total Hours | : | 30L+30P |
    # ---------------------------------------------------------
    for row in rows:
        for cell_index, cell in enumerate(row):
            normalized = _normalize_header(cell)

            if normalized != "totalhours":
                continue

            for value in row[cell_index + 1:]:
                parsed = _parse_total_hours(value)

                if parsed is not None:
                    return parsed

    # ---------------------------------------------------------
    # 4. Engineering Explorations-style format
    #
    # 30L+30P
    # ---------------------------------------------------------
    for row in rows:
        for cell in row:
            if re.search(
                r"\d+\s*[LP]\s*\+\s*\d+\s*[LP]",
                cell,
                flags=re.IGNORECASE,
            ):
                parsed = _parse_total_hours(cell)

                if parsed is not None:
                    return parsed

    # ---------------------------------------------------------
    # 5. Ordinary labelled text
    # ---------------------------------------------------------
    return _extract_number_after_label(
        markdown,
        [
            "Total Hours",
            "Total no. of Teaching hours",
            "TotalNo. of Teaching Hours",
            "Teaching Hours",
        ],
    )
        
def _clean_subject(value: str | None) -> str | None:
    value = _clean(value)

    if not value:
        return None

    value = re.split(
        r"\s+(?:Category|Course\s+Code|Course\s+Credits?|"
        r"Credits|Semester|Programme|Program)\s*:?",
        value,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    return _clean(value)


def extract_metadata(markdown: str) -> AcademicMetadata:
    """Extract academic metadata from Docling Markdown."""

    return AcademicMetadata(
        subject=_extract_subject(markdown),
        course_code=_extract_course_code(markdown),
        programme=_extract_programme(markdown),
        semester=_extract_semester(markdown),
        credits=_extract_credits(markdown),
        teaching_hours=_extract_teaching_hours(markdown),
    )
