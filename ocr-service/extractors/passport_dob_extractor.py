import re

from extractors.base_extractor import BaseExtractor
from models.ocr_region import OCRRegion
from models.ocr_field import OCRField


class PassportDOBExtractor(BaseExtractor):

    DATE_REGEX = re.compile(
        r"\b\d{2}/\d{2}/\d{4}\b"
    )


    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:


        for line in region.lines:

            match = self.DATE_REGEX.search(
                line.text
            )

            if not match:
                continue


            value = match.group()

            year = int(
                value[-4:]
            )


            # DOB usually between 1950-2020
            if 1950 <= year <= 2020:

                return OCRField.from_line(
                    line,
                    value,
                )


        return OCRField.empty()