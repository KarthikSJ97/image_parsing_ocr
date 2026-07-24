import re

from extractors.base_extractor import BaseExtractor
from models.ocr_document import OCRDocument
from models.ocr_field import OCRField


class PassportDOBExtractor(BaseExtractor):

    def extract(
        self,
        document: OCRDocument,
    ) -> OCRField:

        lines = document.lines

        for i, line in enumerate(lines):

            if "DATE OF BIRTH" in line.text.upper():

                for candidate in lines[i + 1:]:

                    match = re.search(
                        r"\d{2}/\d{2}/\d{4}",
                        candidate.text,
                    )

                    if match:
                        return OCRField.from_line(
                            candidate,
                            match.group(),
                        )

        return OCRField.empty()