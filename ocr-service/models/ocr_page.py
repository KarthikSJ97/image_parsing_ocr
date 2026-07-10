from pydantic import BaseModel

from models.ocr_line import OCRLine


class OCRPage(BaseModel):

    page_number: int

    width: int

    height: int

    text: str

    lines: list[OCRLine]

    def find(self, keyword: str) -> OCRLine | None:

        keyword = keyword.lower()

        for line in self.lines:
            if keyword in line.text.lower():
                return line

        return None

    def find_all(self, keyword: str) -> list[OCRLine]:

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
            [
                line
                for line in self.lines
                if line.center_y > reference.center_y
            ],
            key=lambda l: l.center_y,
        )

    def above(
        self,
        reference: OCRLine,
    ) -> list[OCRLine]:

        return sorted(
            [
                line
                for line in self.lines
                if line.center_y < reference.center_y
            ],
            key=lambda l: -l.center_y,
        )

    def right_of(
        self,
        reference: OCRLine,
    ) -> list[OCRLine]:

        return sorted(
            [
                line
                for line in self.lines
                if line.center_x > reference.center_x
            ],
            key=lambda l: l.center_x,
        )

    def left_of(
        self,
        reference: OCRLine,
    ) -> list[OCRLine]:

        return sorted(
            [
                line
                for line in self.lines
                if line.center_x < reference.center_x
            ],
            key=lambda l: -l.center_x,
        )

    def nearest_below(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = self.below(reference)

        if not candidates:
            return None

        return candidates[0]