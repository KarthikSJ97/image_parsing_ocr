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

    @property
    def width(self) -> float:
        return self.right - self.left


    @property
    def height(self) -> float:
        return self.bottom - self.top


    @property
    def area(self) -> float:
        return self.width * self.height

    def overlaps_x(
        self,
        other: "OCRLine",
        tolerance: float = 0,
    ) -> bool:

        return not (
            self.right + tolerance < other.left
            or other.right + tolerance < self.left
        )