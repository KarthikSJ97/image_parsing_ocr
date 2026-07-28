import re

from models.ocr_field import OCRField


class AadhaarDOBExtractor:

    DATE_REGEX = re.compile(
        r"(\d{2}[/-]\d{2}[/-](?:19\d{2}|20\d{2}))"
    )

    YEAR_REGEX = re.compile(
        r"\b(19\d{2}|20\d{2})\b"
    )

    def extract(self, region) -> OCRField:

        lines = region.lines

        #
        # Priority 1
        # DOB / Date of Birth
        #

        for line in lines:

            lower = line.text.lower()

            if (
                "dob" not in lower
                and "date of birth" not in lower
            ):
                continue

            match = self.DATE_REGEX.search(line.text)

            if match:
                return OCRField.from_line(
                    line,
                    match.group(1),
                )

            #
            # OCR sometimes merges text:
            # 00/DOB23/03/1997
            #

            cleaned = re.sub(
                r"[^0-9/-]",
                "",
                line.text,
            )

            match = self.DATE_REGEX.search(cleaned)

            if match:
                return OCRField.from_line(
                    line,
                    match.group(1),
                )

        #
        # Priority 2
        # Year of Birth
        #

        for line in lines:

            if "year of birth" not in line.text.lower():
                continue

            match = self.YEAR_REGEX.search(line.text)

            if match:
                return OCRField.from_line(
                    line,
                    match.group(1),
                )

        #
        # Priority 3
        # Next lines after "Year of Birth"
        #

        for i, line in enumerate(lines):

            if "year of birth" not in line.text.lower():
                continue

            for candidate in lines[i + 1 : i + 3]:

                match = self.YEAR_REGEX.search(
                    candidate.text,
                )

                if match:
                    return OCRField.from_line(
                        candidate,
                        match.group(1),
                    )

        return OCRField.empty()