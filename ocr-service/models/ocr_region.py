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