import math
import re

from pydantic import BaseModel

from models.ocr_line import OCRLine
from utils.text_utils import TextUtils


class OCRPage(BaseModel):

    page_number: int

    width: int | None = None

    height: int | None = None

    text: str

    lines: list[OCRLine]

    # --------------------------------------------------
    # Text Search
    # --------------------------------------------------

    def find(self, keyword: str) -> OCRLine | None:

        for line in self.lines:
            if TextUtils.contains(line.text, keyword):
                return line

        return None

    def find_all(self, keyword: str) -> list[OCRLine]:

        return [
            line
            for line in self.lines
            if TextUtils.contains(line.text, keyword)
        ]

    def fuzzy_find(
        self,
        keyword: str,
        threshold: float = 0.80,
    ) -> OCRLine | None:

        for line in self.lines:
            if TextUtils.fuzzy_contains(
                line.text,
                keyword,
                threshold,
            ):
                return line

        return None

    def regex(self, pattern: str) -> list[OCRLine]:

        regex = re.compile(pattern)

        return [
            line
            for line in self.lines
            if regex.search(line.text)
        ]

    # --------------------------------------------------
    # Spatial Search
    # --------------------------------------------------

    def lines_below(
        self,
        line: OCRLine,
        tolerance: float = 10,
    ) -> list[OCRLine]:

        return sorted(
            [
                candidate
                for candidate in self.lines
                if candidate.center_y > line.center_y
                and abs(candidate.center_x - line.center_x) <= tolerance
            ],
            key=lambda x: x.center_y,
        )

    def lines_above(
        self,
        line: OCRLine,
        tolerance: float = 10,
    ) -> list[OCRLine]:

        return sorted(
            [
                candidate
                for candidate in self.lines
                if candidate.center_y < line.center_y
                and abs(candidate.center_x - line.center_x) <= tolerance
            ],
            key=lambda x: x.center_y,
            reverse=True,
        )

    def lines_right_of(
        self,
        line: OCRLine,
        tolerance: float = 10,
    ) -> list[OCRLine]:

        return sorted(
            [
                candidate
                for candidate in self.lines
                if candidate.center_x > line.center_x
                and abs(candidate.center_y - line.center_y) <= tolerance
            ],
            key=lambda x: x.center_x,
        )

    def lines_left_of(
        self,
        line: OCRLine,
        tolerance: float = 10,
    ) -> list[OCRLine]:

        return sorted(
            [
                candidate
                for candidate in self.lines
                if candidate.center_x < line.center_x
                and abs(candidate.center_y - line.center_y) <= tolerance
            ],
            key=lambda x: x.center_x,
            reverse=True,
        )

    # --------------------------------------------------
    # Nearest neighbours
    # --------------------------------------------------

    def nearest_below(self, line: OCRLine) -> OCRLine | None:

        lines = self.lines_below(line)

        return lines[0] if lines else None

    def nearest_above(self, line: OCRLine) -> OCRLine | None:

        lines = self.lines_above(line)

        return lines[0] if lines else None

    def nearest_right(self, line: OCRLine) -> OCRLine | None:

        lines = self.lines_right_of(line)

        return lines[0] if lines else None

    def nearest_left(self, line: OCRLine) -> OCRLine | None:

        lines = self.lines_left_of(line)

        return lines[0] if lines else None

    def nearest(self, line: OCRLine) -> OCRLine | None:

        best = None
        best_distance = float("inf")

        for candidate in self.lines:

            if candidate == line:
                continue

            distance = math.sqrt(
                (candidate.center_x - line.center_x) ** 2
                + (candidate.center_y - line.center_y) ** 2
            )

            if distance < best_distance:
                best_distance = distance
                best = candidate

        return best