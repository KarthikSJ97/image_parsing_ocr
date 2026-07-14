import re

from models.ocr_field import OCRField


class YearExtractor:

    YEAR_REGEX = re.compile(r"\b(19\d{2}|20\d{2})\b")

    def extract(self, region):

        #
        # Highest priority:
        # "Year of Birth : 1967"
        #

        for line in region.lines:

            text = line.text.lower()

            if "year of birth" in text:

                match = self.YEAR_REGEX.search(line.text)

                if match:
                    return OCRField.from_line(
                        line,
                        match.group(1),
                    )

        #
        # Next priority:
        # lines immediately after "Year of Birth"
        #

        lines = region.lines

        for i, line in enumerate(lines):

            if "year of birth" in line.text.lower():

                for nxt in lines[i + 1 : i + 3]:

                    match = self.YEAR_REGEX.search(nxt.text)

                    if match:
                        return OCRField.from_line(
                            nxt,
                            match.group(1),
                        )

        #
        # Last priority:
        # DOB
        #

        for line in lines:

            if "dob" in line.text.lower():

                years = self.YEAR_REGEX.findall(line.text)

                if years:
                    return OCRField.from_line(
                        line,
                        years[-1],
                    )

        return OCRField.empty()