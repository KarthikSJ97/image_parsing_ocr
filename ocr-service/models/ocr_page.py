from typing import List

from pydantic import BaseModel

from models.ocr_line import OCRLine


class OCRPage(BaseModel):

    page_number: int

    width: int | None = None
    
    height: int | None = None

    text: str

    lines: list[OCRLine]