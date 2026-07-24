from pydantic import BaseModel

from models.ocr_line import OCRLine


class OCRField(BaseModel):

    value: str | None = None

    confidence: float = 0.0

    source: OCRLine | None = None

    source_lines: list[OCRLine] = []

    @classmethod
    def from_line(
        cls,
        line: OCRLine | None,
        value: str | None = None,
    ):
        if line is None:
            return cls()

        return cls(
            value=value or line.text,
            confidence=line.confidence,
            source=line,
            source_lines=[line],
        )

    @classmethod
    def from_lines(
        cls,
        lines: list[OCRLine],
        value: str,
    ):

        if not lines:
            return cls()

        return cls(
            value=value,
            confidence=min(
                line.confidence
                for line in lines
            ),
            source=lines[0],
            source_lines=lines,
        )
        
    @classmethod
    def empty(cls):
        return cls()