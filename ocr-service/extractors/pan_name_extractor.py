import re

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class PanNameExtractor(BaseExtractor):

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

    PAN_REGEX = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")

    DATE_REGEX = re.compile(r"\d{2}[/-]\d{2}[/-]\d{4}")

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:

        candidates = []

        for line in region.lines:

            text = line.text.strip()

            if not text:
                continue

            # Ignore weak OCR
            if line.confidence < 0.90:
                continue

            upper = text.upper()

            # Skip dates
            if self.DATE_REGEX.search(upper):
                continue

            # Skip PAN number
            if self.PAN_REGEX.fullmatch(
                upper.replace(" ", "")
            ):
                continue

            # Skip headers/labels
            if any(word in upper for word in self.GOVERNMENT_WORDS):
                continue

            words = upper.split()

            # Must look like a person's name
            if len(words) < 2:
                continue

            if not all(word.isalpha() for word in words):
                continue

            candidates.append(line)

        if not candidates:
            return OCRField.empty()

        # First valid candidate
        return OCRField.from_line(
            candidates[0],
            candidates[0].text,
        )