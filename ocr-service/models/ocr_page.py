from typing import List

from pydantic import BaseModel

from models.ocr_line import OCRLine


class OCRPage(BaseModel):
    page_number: int
    lines: List[OCRLine]