from __future__ import annotations

import re
from pathlib import Path

from docling.document_converter import DocumentConverter


class AcademicDocumentParser:
    """Parse academic PDFs into normalized Markdown using Docling."""

    def __init__(self) -> None:
        self.converter = DocumentConverter()

    def parse(self, pdf_path: str | Path) -> str:
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        result = self.converter.convert(str(pdf_path))

        markdown = result.document.export_to_markdown()

        return self.normalize(markdown)

    @staticmethod
    def normalize(markdown: str) -> str:
        """Normalize common Docling artifacts."""

        text = markdown.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Remove Docling image placeholders.
        text = re.sub(
            r"<!--\s*image\s*-->",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # Normalize spaces without destroying line boundaries.
        text = re.sub(r"[ \t]+", " ", text)

        # Remove excessive blank lines.
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()