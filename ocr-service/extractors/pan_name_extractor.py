import re

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class PanNameExtractor(BaseExtractor):

    def extract(self, region: OCRRegion) -> OCRField:

        for line in region.lines:

            text = line.text.strip()

            if not text:
                continue

            lower = text.lower()

            # Skip government header
            if (
                "govt" in lower
                or "government" in lower
                or "income tax" in lower
            ):
                continue

            # Skip OCR garbage
            if lower in {"hrcor"}:
                continue

            # Stop before DOB
            if re.search(
                r"\d{2}[/-]\d{2}[/-]\d{4}",
                text,
            ):
                break

            # Skip father label if present
            if (
                "father" in lower
                or "son of" in lower
                or "daughter of" in lower
            ):
                continue

            # Skip PAN label
            if "permanent account number" in lower:
                continue

            # Skip PAN number
            if re.fullmatch(
                r"[A-Z]{5}[0-9]{4}[A-Z]",
                text.replace(" ", ""),
            ):
                continue

            # Name validation
            alpha_chars = sum(
                c.isalpha()
                for c in text
            )

            if alpha_chars >= 3:
                return OCRField.from_line(
                    line,
                    text,
                )

        return OCRField.empty()