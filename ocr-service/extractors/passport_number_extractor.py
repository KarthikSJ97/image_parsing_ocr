import re

from extractors.base_extractor import BaseExtractor
from models.ocr_document import OCRDocument
from models.ocr_field import OCRField


class PassportNumberExtractor(BaseExtractor):

    def extract(
        self,
        document: OCRDocument,
    ) -> OCRField:

        pattern = r"\b[A-Z][0-9]{7}\b"

        for line in document.lines:

            match = re.search(
                pattern,
                line.text.upper(),
            )

            if match:
                return OCRField.from_line(
                    line,
                    match.group(),
                )

        return OCRField.empty()