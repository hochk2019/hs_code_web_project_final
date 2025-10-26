"""Trích xuất văn bản từ PDF."""

from __future__ import annotations

from pathlib import Path

import pdfplumber
from PIL import Image
import pytesseract


class PDFExtractor:
    """Hỗ trợ trích xuất văn bản từ PDF thường và PDF scan."""

    def extract_text(self, path: Path, *, ocr: bool = True) -> str:
        """Đọc toàn bộ nội dung PDF và trả về chuỗi Unicode."""

        text_parts: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                if text.strip():
                    text_parts.append(text)
                elif ocr:
                    image = page.to_image(resolution=300).original
                    pil_image = Image.fromarray(image)
                    text_parts.append(pytesseract.image_to_string(pil_image, lang="vie"))
        return "\n".join(filter(None, (part.strip() for part in text_parts)))
