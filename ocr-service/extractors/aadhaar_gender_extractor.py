import re

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class AadhaarGenderExtractor(BaseExtractor):

    PATTERN = re.compile(
        r"\b(male|female|transgender)\b",
        re.IGNORECASE,
    )

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:

        for line in region.lines:

            match = self.PATTERN.search(line.text)

            if match:
                return OCRField.from_line(
                    line,
                    match.group(1).title(),
                )

        return OCRField.empty()