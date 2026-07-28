import re

from extractors.base_extractor import BaseExtractor
from models.ocr_region import OCRRegion
from models.ocr_field import OCRField


class PassportExpiryDateExtractor(BaseExtractor):

    DATE_REGEX = re.compile(
        r"\b\d{2}/\d{2}/\d{4}\b"
    )


    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:


        dates = []


        for line in region.lines:

            for match in self.DATE_REGEX.finditer(
                line.text
            ):

                value = match.group()

                year = int(
                    value[-4:]
                )


                # Passport expiry usually future
                if year >= 2024:

                    dates.append(
                        (
                            line,
                            value,
                        )
                    )


        if not dates:
            return OCRField.empty()


        line, value = max(
            dates,
            key=lambda x: x[0].center_y,
        )


        return OCRField.from_line(
            line,
            value,
        )