import re

from extractors.base_extractor import BaseExtractor
from models.ocr_document import OCRDocument
from models.ocr_field import OCRField


class AadhaarNumberExtractor(BaseExtractor):

    PATTERN = re.compile(
        r"\b\d{4}\s?\d{4}\s?\d{4}\b"
    )

    def extract(
        self,
        document: OCRDocument,
    ) -> OCRField:

        for line in document.lines():

            match = self.PATTERN.search(
                line.text,
            )

            if not match:
                continue

            number = match.group()

            if number.startswith("1800"):
                continue

            number = re.sub(
                r"\s+",
                " ",
                number,
            )

            return OCRField.from_line(
                line,
                number,
            )

        return OCRField.empty()