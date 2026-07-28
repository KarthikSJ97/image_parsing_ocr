import re

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class DrivingLicenseValidTillExtractor(BaseExtractor):

    DATE_REGEX = re.compile(
        r"(\d{2}[/-]\d{2}[/-]\d{4})"
    )

    KEYWORDS = (
        "valid till",
        "valid upto",
        "valid until",
        "validity",
    )

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:

        lines = region.lines

        #
        # Priority 1
        # VALID TILL : 31/01/2026(NT)
        #

        for line in lines:

            lower = line.text.lower()

            if not any(
                keyword in lower
                for keyword in self.KEYWORDS
            ):
                continue

            match = self.DATE_REGEX.search(
                line.text,
            )

            if match:
                return OCRField.from_line(
                    line,
                    match.group(1),
                )

        #
        # Priority 2
        # Date on next line
        #

        for index, line in enumerate(lines):

            lower = line.text.lower()

            if not any(
                keyword in lower
                for keyword in self.KEYWORDS
            ):
                continue

            for candidate in lines[index + 1:index + 3]:

                match = self.DATE_REGEX.search(
                    candidate.text,
                )

                if match:
                    return OCRField.from_line(
                        candidate,
                        match.group(1),
                    )

        return OCRField.empty()