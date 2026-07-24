import re

from extractors.base_extractor import BaseExtractor
from models.ocr_region import OCRRegion
from models.ocr_field import OCRField


class PassportExpiryDateExtractor(BaseExtractor):

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:

        expiry_label = None

        # Find the "Date of Expiry" label
        for line in region.lines:
            if "DATE OF EXPIRY" in line.text.upper():
                expiry_label = line
                break

        if expiry_label is None:
            return OCRField.empty()

        candidates = []

        # Find all dates below the label
        for line in region.lines:

            match = re.search(
                r"\d{2}/\d{2}/\d{4}",
                line.text,
            )

            if not match:
                continue

            # Only consider dates below the label
            if line.center_y <= expiry_label.center_y:
                continue

            candidates.append(
                (
                    line,
                    match.group(),
                )
            )

        if not candidates:
            return OCRField.empty()

        # Pick the right-most date (Expiry Date)
        line, value = max(
            candidates,
            key=lambda x: x[0].center_x,
        )

        return OCRField.from_line(
            line,
            value,
        )