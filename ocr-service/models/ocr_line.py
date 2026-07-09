from typing import List

from pydantic import BaseModel

from models.point import Point


class OCRLine(BaseModel):
    text: str
    confidence: float
    polygon: List[Point]