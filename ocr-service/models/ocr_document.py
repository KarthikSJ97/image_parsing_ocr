from typing import List

from pydantic import BaseModel

from models.ocr_page import OCRPage


class OCRDocument(BaseModel):
    pages: List[OCRPage]

    @property
    def full_text(self) -> str:
        return "\n".join(
            line.text
            for page in self.pages
            for line in page.lines
        )