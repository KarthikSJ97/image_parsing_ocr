import re

from extractors.base_extractor import BaseExtractor
from models.ocr_document import OCRDocument
from models.ocr_field import OCRField


class PassportNationalityExtractor(BaseExtractor):

    def extract(
        self,
        document: OCRDocument,
    ) -> OCRField:

        lines = document.lines

        for i, line in enumerate(lines):

            if "NATIONALITY" in line.text.upper():

                for candidate in lines[i + 1:i + 6]:

                    if re.fullmatch(
                        r"[A-Z ]+",
                        candidate.text.upper(),
                    ):
                        return OCRField.from_line(candidate)

        return OCRField.empty()