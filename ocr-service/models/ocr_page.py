from pydantic import BaseModel

from models.ocr_line import OCRLine


class OCRPage(BaseModel):

    page_number: int

    width: int

    height: int

    text: str

    lines: list[OCRLine]

    ####################################################################
    # Text Search
    ####################################################################

    def find(self, keyword: str) -> OCRLine | None:

        keyword = keyword.lower()

        for line in self.lines:
            if keyword in line.text.lower():
                return line

        return None

    def find_all(
        self,
        keyword: str,
    ) -> list[OCRLine]:

        keyword = keyword.lower()

        return [
            line
            for line in self.lines
            if keyword in line.text.lower()
        ]

    def fuzzy_find(
        self,
        keyword: str,
        threshold: float = 0.80,
    ) -> OCRLine | None:

        from utils.text_utils import TextUtils

        for line in self.lines:

            if TextUtils.fuzzy_contains(
                line.text,
                keyword,
                threshold,
            ):
                return line

        return None

    def regex(
        self,
        pattern: str,
    ) -> list[OCRLine]:

        import re

        return [
            line
            for line in self.lines
            if re.search(pattern, line.text)
        ]

    ####################################################################
    # Spatial Helpers
    ####################################################################

    def below(
        self,
        reference: OCRLine,
    ) -> list[OCRLine]:

        return sorted(
            (
                line
                for line in self.lines
                if line.center_y > reference.center_y
            ),
            key=lambda l: l.center_y,
        )

    def above(
        self,
        reference: OCRLine,
    ) -> list[OCRLine]:

        return sorted(
            (
                line
                for line in self.lines
                if line.center_y < reference.center_y
            ),
            key=lambda l: -l.center_y,
        )

    def right_of(
        self,
        reference: OCRLine,
    ) -> list[OCRLine]:

        return sorted(
            (
                line
                for line in self.lines
                if line.center_x > reference.center_x
            ),
            key=lambda l: l.center_x,
        )

    def left_of(
        self,
        reference: OCRLine,
    ) -> list[OCRLine]:

        return sorted(
            (
                line
                for line in self.lines
                if line.center_x < reference.center_x
            ),
            key=lambda l: -l.center_x,
        )

    ####################################################################
    # Geometry Helpers
    ####################################################################

    def overlaps_x(
        self,
        reference: OCRLine,
        tolerance: float = 10,
    ) -> list[OCRLine]:

        return [
            line
            for line in self.lines
            if (
                line.right >= reference.left - tolerance
                and line.left <= reference.right + tolerance
            )
        ]

    def overlaps_y(
        self,
        reference: OCRLine,
        tolerance: float = 5,
    ) -> list[OCRLine]:

        return [
            line
            for line in self.lines
            if (
                line.bottom >= reference.top - tolerance
                and line.top <= reference.bottom + tolerance
            )
        ]

    def below_aligned(
        self,
        reference: OCRLine,
        tolerance: float = 10,
    ) -> list[OCRLine]:

        return sorted(
            (
                line
                for line in self.below(reference)
                if (
                    line.right >= reference.left - tolerance
                    and line.left <= reference.right + tolerance
                )
            ),
            key=lambda l: l.center_y,
        )

    def above_aligned(
        self,
        reference: OCRLine,
        tolerance: float = 10,
    ) -> list[OCRLine]:

        return sorted(
            (
                line
                for line in self.above(reference)
                if (
                    line.right >= reference.left - tolerance
                    and line.left <= reference.right + tolerance
                )
            ),
            key=lambda l: -l.center_y,
        )

    def right_same_row(
        self,
        reference: OCRLine,
        tolerance: float = 8,
    ) -> list[OCRLine]:

        return sorted(
            (
                line
                for line in self.right_of(reference)
                if abs(line.center_y - reference.center_y) <= tolerance
            ),
            key=lambda l: l.center_x,
        )

    def left_same_row(
        self,
        reference: OCRLine,
        tolerance: float = 8,
    ) -> list[OCRLine]:

        return sorted(
            (
                line
                for line in self.left_of(reference)
                if abs(line.center_y - reference.center_y) <= tolerance
            ),
            key=lambda l: -l.center_x,
        )

    ####################################################################
    # Nearest Helpers
    ####################################################################

    def nearest_below(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = self.below(reference)

        return candidates[0] if candidates else None

    def nearest_above(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = self.above(reference)

        return candidates[0] if candidates else None

    def nearest_below_aligned(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = self.below_aligned(reference)

        return candidates[0] if candidates else None

    def nearest_right(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = self.right_of(reference)

        return candidates[0] if candidates else None

    def nearest_right_same_row(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = self.right_same_row(reference)

        return candidates[0] if candidates else None