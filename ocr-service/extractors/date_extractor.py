import re

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class DateExtractor(BaseExtractor):

    DATE_REGEX = re.compile(
        r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"
    )

    def extract(self, region: OCRRegion) -> OCRField:

        for line in region.lines:

            match = self.DATE_REGEX.search(line.text)

            if match:
                return OCRField.from_line(
                    line,
                    match.group(),
                )

        return OCRField.empty()