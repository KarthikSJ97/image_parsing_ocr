import re

from models.ocr_document import OCRDocument
from models.ocr_field import OCRField
from extractors.base_extractor import BaseExtractor


class DrivingLicenseNumberExtractor(BaseExtractor):

    LICENSE_PATTERN = re.compile(
        r"[A-Z]{2}\d{2}\s?\d{11}",
        re.IGNORECASE,
    )

    def extract(
        self,
        document: OCRDocument,
    ) -> OCRField:

        for line in document.lines:

            match = self.LICENSE_PATTERN.search(line.text)

            if match:
                return OCRField.from_line(
                    line,
                    match.group(0).strip(),
                )

        return OCRField.empty()