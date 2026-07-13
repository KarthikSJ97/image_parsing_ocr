from models.ocr_line import OCRLine


class OCRRegion:

    def __init__(
        self,
        lines: list[OCRLine],
    ):
        self._lines = lines


    def lines(self) -> list[OCRLine]:
        return self._lines


    def text(self) -> str:
        return "\n".join(
            line.text
            for line in self._lines
        )


    def find(
        self,
        keyword: str,
    ) -> OCRLine | None:

        keyword = keyword.lower()

        for line in self._lines:
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
            for line in self._lines
            if keyword in line.text.lower()
        ]


    def regex(
        self,
        pattern: str,
    ) -> list[OCRLine]:

        import re

        return [
            line
            for line in self._lines
            if re.search(
                pattern,
                line.text,
                re.IGNORECASE,
            )
        ]

    def nearest_above(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = [
            line
            for line in self._lines
            if line.center_y < reference.center_y
        ]

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda line: line.center_y,
        )


    def nearest_below(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = [
            line
            for line in self._lines
            if line.center_y > reference.center_y
        ]

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda line: line.center_y,
        )


    def nearest_left(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = [
            line
            for line in self._lines
            if line.center_x < reference.center_x
        ]

        if not candidates:
            return None

        return max(
            candidates,
            key=lambda line: line.center_x,
        )


    def nearest_right(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        candidates = [
            line
            for line in self._lines
            if line.center_x > reference.center_x
        ]

        if not candidates:
            return None

        return min(
            candidates,
            key=lambda line: line.center_x,
        )    

    @property
    def is_empty(self) -> bool:
        return len(self.lines) == 0    