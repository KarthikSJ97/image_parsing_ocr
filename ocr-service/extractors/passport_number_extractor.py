import re

from extractors.base_extractor import BaseExtractor
from models.ocr_region import OCRRegion
from models.ocr_field import OCRField


class PassportNumberExtractor(BaseExtractor):

    PASSPORT_REGEX = re.compile(r"\b[A-Z][0-9]{7}\b")

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:

        for line in region.lines:

            match = self.PASSPORT_REGEX.search(
                line.text.upper(),
            )

            if match:
                return OCRField.from_line(
                    line,
                    match.group(),
                )

        return OCRField.empty()