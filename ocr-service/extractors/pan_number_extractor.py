import re

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class PanNumberExtractor(BaseExtractor):

    PAN_REGEX = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")

    def extract(self, region: OCRRegion) -> OCRField:

        for line in region.lines:

            match = self.PAN_REGEX.search(line.text.upper())

            if match:
                return OCRField.from_line(
                    line,
                    match.group(),
                )

        return OCRField.empty()