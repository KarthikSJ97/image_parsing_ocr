import re

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class PanFatherNameExtractor(BaseExtractor):

    PAN_REGEX = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")

    DATE_REGEX = re.compile(r"\d{2}[/-]\d{2}[/-]\d{4}")

    GOVERNMENT_WORDS = {
        "INCOME",
        "TAX",
        "DEPARTMENT",
        "GOVT",
        "GOVERNMENT",
        "INDIA",
        "PERMANENT",
        "ACCOUNT",
        "NUMBER",
        "CARD",
        "SIGNATURE",
        "NAME",
        "FATHER",
        "DATE",
        "BIRTH",
    }

    def extract(
        self,
        region: OCRRegion,
        person_name: str | None = None,
    ) -> OCRField:

        if not person_name:
            return OCRField.empty()

        name_found = False

        for line in region.lines:

            text = line.text.strip()

            if not text:
                continue

            if line.confidence < 0.90:
                continue

            upper = text.upper()

            if upper == person_name.upper():
                name_found = True
                continue

            if not name_found:
                continue

            if self.DATE_REGEX.search(upper):
                break

            if self.PAN_REGEX.fullmatch(
                upper.replace(" ", "")
            ):
                continue

            if any(word in upper for word in self.GOVERNMENT_WORDS):
                continue

            words = upper.split()

            if len(words) < 2:
                continue

            if not all(word.isalpha() for word in words):
                continue

            return OCRField.from_line(
                line,
                text,
            )

        return OCRField.empty()