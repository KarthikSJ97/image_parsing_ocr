import re

from extractors.base_extractor import BaseExtractor
from models.ocr_document import OCRDocument
from models.ocr_field import OCRField


class DrivingLicenseDOIExtractor(BaseExtractor):

    DATE_REGEX = r"\d{2}[/-]\d{2}[/-]\d{4}"

    def extract(
        self,
        document: OCRDocument,
    ) -> OCRField:

        lines = document.lines

        for i, line in enumerate(lines):

            if "DOI" in line.text.upper():

                match = re.search(
                    self.DATE_REGEX,
                    line.text,
                )

                if match:
                    return OCRField.from_line(
                        line,
                        match.group(),
                    )

                if i + 1 < len(lines):

                    match = re.search(
                        self.DATE_REGEX,
                        lines[i + 1].text,
                    )

                    if match:
                        return OCRField.from_line(
                            lines[i + 1],
                            match.group(),
                        )

        return OCRField.empty()