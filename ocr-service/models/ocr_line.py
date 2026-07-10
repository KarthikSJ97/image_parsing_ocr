from pydantic import BaseModel

from models.point import Point


class OCRLine(BaseModel):
    text: str

    confidence: float

    polygon: list[Point]

    left: float
    top: float
    right: float
    bottom: float

    center_x: float
    center_y: float