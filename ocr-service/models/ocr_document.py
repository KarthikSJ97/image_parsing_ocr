from typing import List

from pydantic import BaseModel

from models.ocr_page import OCRPage


class OCRDocument(BaseModel):

    pages: list[OCRPage]

    full_text: str

    average_confidence: float