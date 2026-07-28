import re

from extractors.base_extractor import BaseExtractor
from models.ocr_region import OCRRegion
from models.ocr_field import OCRField


class PassportNameExtractor(BaseExtractor):

    NAME_PATTERN = re.compile(
        r"^[A-Z]+(?:\s+[A-Z]+)+$"
    )

    IGNORE_WORDS = {
        "SURNAME",
        "GIVEN",
        "NAME",
        "NATIONALITY",
        "INDIAN",
        "INDIA",
        "DATE",
        "ISSUE",
        "EXPIRY",
        "BIRTH",
        "SEX",
        "PLACE",
    }


    def extract(
        self,
        document: OCRRegion,
    ) -> OCRField:

        lines = document.lines

        candidates = []

        for line in lines:

            text = (
                line.text
                .upper()
                .strip()
            )


            # Ignore MRZ
            if "<" in text:
                continue


            # Ignore dates/numbers
            if any(
                char.isdigit()
                for char in text
            ):
                continue


            words = text.split()

            if not words:
                continue


            if any(
                word in self.IGNORE_WORDS
                for word in words
            ):
                continue


            if self.NAME_PATTERN.match(text):

                candidates.append(line)


        if not candidates:
            return OCRField.empty()


        # Select candidate between surname and nationality area
        best = max(
            candidates,
            key=lambda x: x.center_y,
        )


        return OCRField.from_line(
            best,
            best.text.strip(),
        )