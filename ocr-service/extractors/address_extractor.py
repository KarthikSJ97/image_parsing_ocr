import re
from difflib import SequenceMatcher

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class AddressExtractor(BaseExtractor):

    def extract(
        self,
        region: OCRRegion,
        person_name: str | None = None,
    ) -> OCRField:

        selected = []
        seen_pincodes = set()

        for line in region.lines:

            text = line.text.strip()

            if not text:
                continue

            lower = text.lower()

            # ---------------------------------------------------------
            # Remove person's name (fuzzy match to handle OCR mistakes)
            # ---------------------------------------------------------
            if person_name:
                similarity = SequenceMatcher(
                    None,
                    lower,
                    person_name.lower(),
                ).ratio()

                if similarity >= 0.75:
                    continue

            # ---------------------------------------------------------
            # Skip Aadhaar number
            # ---------------------------------------------------------
            if re.search(r"\d{4}\s*\d{4}\s*\d{4}", text):
                continue

            # ---------------------------------------------------------
            # Skip DOB / Year of Birth
            # ---------------------------------------------------------
            if (
                "birth" in lower
                or "year of birth" in lower
                or "dob" in lower
            ):
                continue

            # ---------------------------------------------------------
            # Skip gender
            # ---------------------------------------------------------
            if (
                "male" in lower
                or "female" in lower
                or "transgender" in lower
            ):
                continue

            # ---------------------------------------------------------
            # Skip obvious OCR garbage
            # ---------------------------------------------------------
            if (
                line.confidence < 0.60
                and not re.search(r"\d{6}", text)
            ):
                continue

            # ---------------------------------------------------------
            # Normalize pincode-only OCR
            # Example:
            #   rgw-560087 -> 560087
            # ---------------------------------------------------------
            pincode_match = re.search(r"\b\d{6}\b", text)

            if pincode_match:
                pincode = pincode_match.group()

                if pincode in seen_pincodes:
                    continue

                seen_pincodes.add(pincode)

                if text != pincode:
                    text = pincode

            # ---------------------------------------------------------
            # Ignore tiny OCR fragments
            # ---------------------------------------------------------
            if len(text) <= 1:
                continue

            # Store cleaned text
            line.text = text
            selected.append(line)

        if not selected:
            return OCRField.empty()

        value = ", ".join(
            line.text
            for line in selected
        )

        # Cleanup punctuation
        value = re.sub(r",\s*,+", ", ", value)
        value = re.sub(r"\s+", " ", value)
        value = value.strip(" ,")

        return OCRField.from_lines(
            selected,
            value,
        )