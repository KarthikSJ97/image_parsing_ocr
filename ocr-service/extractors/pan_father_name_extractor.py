import re

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class PanFatherNameExtractor(BaseExtractor):

    def extract(
        self,
        region: OCRRegion,
        person_name: str | None = None,
    ) -> OCRField:

        name_found = False

        for line in region.lines:

            text = line.text.strip()

            if not text:
                continue

            lower = text.lower()

            # Skip government headers
            if (
                "govt" in lower
                or "government" in lower
                or "income tax" in lower
            ):
                continue

            # Skip PAN logo OCR garbage
            if lower in {
                "hrcor",
                "pan",
                "permanent account number",
            }:
                continue

            # Stop when DOB starts
            if re.search(
                r"\d{2}[/-]\d{2}[/-]\d{4}",
                text,
            ):
                break

            # Skip extracted person's name
            if (
                person_name
                and text.lower() == person_name.lower()
            ):
                name_found = True
                continue

            # We only search after person's name
            if not name_found:
                continue

            # Skip PAN number
            if re.fullmatch(
                r"[A-Z]{5}[0-9]{4}[A-Z]",
                text.replace(" ", ""),
            ):
                continue

            # Basic name validation
            alpha_count = sum(
                c.isalpha()
                for c in text
            )

            if alpha_count >= 3:
                return OCRField.from_line(
                    line,
                    text,
                )

        return OCRField.empty()