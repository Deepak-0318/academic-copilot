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


def _clean(value: str | None) -> str | None:
    if not value:
        return None

    value = re.sub(r"\s+", " ", value).strip()

    return value or None


def _extract_field(
    text: str,
    field: str,
    next_fields: list[str],
) -> str | None:

    escaped_field = re.escape(field)

    next_pattern = "|".join(
        re.escape(item)
        for item in next_fields
    )

    pattern = (
        rf"{escaped_field}"
        rf"\s*(?::|\|)?\s*"
        rf"(.+?)"
        rf"(?=\s*(?:{next_pattern})\b|$)"
    )

    match = re.search(
        pattern,
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return None

    return _clean(match.group(1))


def _parse_int(value: str | None) -> int | None:
    if value is None:
        return None

    match = re.search(r"\d+", value)

    if not match:
        return None

    return int(match.group())


def _parse_semester(value: str | None) -> int | None:
    if value is None:
        return None

    value = value.strip().upper()

    roman = {
        "I": 1,
        "II": 2,
        "III": 3,
        "IV": 4,
        "V": 5,
        "VI": 6,
        "VII": 7,
        "VIII": 8,
    }

    if value in roman:
        return roman[value]

    return _parse_int(value)


def extract_metadata(markdown: str) -> AcademicMetadata:
    """Extract academic metadata from Docling Markdown."""

    # Course code
    course_code_match = re.search(
        r"Course Code:\s*([A-Za-z0-9_-]+)",
        markdown,
        flags=re.IGNORECASE,
    )

    course_code = (
        course_code_match.group(1).strip()
        if course_code_match
        else None
    )

    # Programme
    programme_match = re.search(
        r"Name of the Programme:\s*(.*?)\s+Name of the Course:",
        markdown,
        flags=re.IGNORECASE | re.DOTALL,
    )

    programme = (
        _clean(programme_match.group(1))
        if programme_match
        else None
    )

    # Course / subject
    subject_match = re.search(
        r"Name of the Course:\s*(.*?)\s+Semester:",
        markdown,
        flags=re.IGNORECASE | re.DOTALL,
    )

    subject = (
        _clean(subject_match.group(1))
        if subject_match
        else None
    )

    # Semester
    semester_match = re.search(
        r"Semester:\s*([IVX]+|\d+)",
        markdown,
        flags=re.IGNORECASE,
    )

    semester = (
        _parse_semester(semester_match.group(1))
        if semester_match
        else None
    )

    # Credits
    #
    # Actual Docling structure:
    #
    # | Course credit No. of hours per week ... |
    # | 4 2+0+4 | ... | Total no. of Teaching hours |
    # | ... | ... | 90 |
    #
    credits_match = re.search(
        r"\|\s*(\d+)\s+\d+\+\d+\+\d+\s*\|",
        markdown,
    )

    credits = (
        int(credits_match.group(1))
        if credits_match
        else None
    )

    teaching_hours = _extract_teaching_hours(markdown)

    return AcademicMetadata(
        subject=subject,
        course_code=course_code,
        programme=programme,
        semester=semester,
        credits=credits,
        teaching_hours=teaching_hours,
    )
    
def _extract_teaching_hours(markdown: str) -> int | None:
    """
    Extract total teaching hours from the academic metadata table.
    """

    lines = markdown.splitlines()

    for index, line in enumerate(lines):
        if "Total no. of Teaching hours" not in line:
            continue

        # The value is in the following table row.
        if index + 1 >= len(lines):
            continue

        value_line = lines[index + 1]

        # Example:
        # | 4 2+0+4 | 4 2+0+4 | 90 |
        cells = [
            cell.strip()
            for cell in value_line.split("|")
            if cell.strip()
        ]

        if not cells:
            continue

        # The final cell is the total teaching hours.
        last_cell = cells[-1]

        match = re.search(r"\b\d+\b", last_cell)

        if match:
            return int(match.group())

    return None