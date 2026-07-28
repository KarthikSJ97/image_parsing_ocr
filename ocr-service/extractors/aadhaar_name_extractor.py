import re

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class AadhaarNameExtractor(BaseExtractor):

    BLACKLIST = (
        "government",
        "india",
        "uidai",
        "aadhaar",
        "authority",
        "identification",
        "unique",
        "enrol",
        "enrollment",
        "information",
        "address",
        "dob",
        "male",
        "female",
    )

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:

        #
        # Aadhaar layout:
        #
        # Name
        # DOB
        # Gender
        #

        for i, line in enumerate(region.lines):

            text = line.text.strip()

            lower = text.lower()

            if any(word in lower for word in self.BLACKLIST):
                continue

            if re.search(r"\d", text):
                continue

            words = text.split()

            if len(words) < 2:
                continue

            #
            # Look below.
            #

            for nxt in region.lines[i + 1:i + 3]:

                l = nxt.text.lower()

                if (
                    "dob" in l
                    or "year of birth" in l
                    or "male" in l
                    or "female" in l
                    or re.search(r"\d{2}/\d{2}/\d{4}", l)
                ):
                    return OCRField.from_line(
                        line,
                        text,
                    )

        return OCRField.empty()