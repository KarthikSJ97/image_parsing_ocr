import re
from difflib import SequenceMatcher

from extractors.base_extractor import BaseExtractor
from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class AadhaarAddressExtractor(BaseExtractor):

    FOOTER_KEYWORDS = (
        "uidai",
        "www.",
        "http",
        "help@",
        "1947",
        "1800",
        "aadhaar",
        "government of india",
        "unique identification",
        "vid",
        "virtual id",
        "qr",
    )

    PINCODE_REGEX = re.compile(r"\b\d{6}\b")

    def extract(
        self,
        region: OCRRegion,
        person_name: str | None = None,
    ) -> OCRField:

        selected = []
        seen_pincodes = set()
        found_pincode = False

        previous = None

        for line in region.lines:

            text = line.text.strip()

            if not text:
                continue

            lower = text.lower()

            # ---------------------------------------------------------
            # Footer reached -> address ends
            # ---------------------------------------------------------
            if any(
                keyword in lower
                for keyword in self.FOOTER_KEYWORDS
            ):
                break

            # ---------------------------------------------------------
            # Large vertical gap usually indicates footer
            # ---------------------------------------------------------
            if previous is not None:

                gap = line.top - previous.bottom
                height = max(
                    previous.bottom - previous.top,
                    1,
                )

                if gap > height * 2.5:
                    break

            # ---------------------------------------------------------
            # Remove person's name
            # ---------------------------------------------------------
            if person_name:

                similarity = SequenceMatcher(
                    None,
                    lower,
                    person_name.lower(),
                ).ratio()

                if similarity >= 0.75:
                    previous = line
                    continue

            # ---------------------------------------------------------
            # Aadhaar Number
            # ---------------------------------------------------------
            if re.search(
                r"\d{4}\s*\d{4}\s*\d{4}",
                text,
            ):
                previous = line
                continue

            # ---------------------------------------------------------
            # DOB / Gender
            # ---------------------------------------------------------
            if (
                "dob" in lower
                or "birth" in lower
                or "male" in lower
                or "female" in lower
                or "transgender" in lower
            ):
                previous = line
                continue

            # ---------------------------------------------------------
            # OCR garbage
            # ---------------------------------------------------------
            if (
                line.confidence < 0.60
                and not self.PINCODE_REGEX.search(text)
            ):
                previous = line
                continue

            # ---------------------------------------------------------
            # Extract PIN
            # ---------------------------------------------------------
            match = self.PINCODE_REGEX.search(text)

            if match:

                pin = match.group()

                if pin in seen_pincodes:
                    previous = line
                    continue

                seen_pincodes.add(pin)
                found_pincode = True

                text = pin

            # ---------------------------------------------------------
            # Ignore tiny fragments
            # ---------------------------------------------------------
            if len(text) <= 1:
                previous = line
                continue

            line.text = text
            selected.append(line)
            previous = line

            # ---------------------------------------------------------
            # Usually address ends immediately after PIN
            # ---------------------------------------------------------
            if found_pincode:
                break

        if not selected:
            return OCRField.empty()

        value = ", ".join(
            line.text
            for line in selected
        )

        value = re.sub(
            r",\s*,+",
            ", ",
            value,
        )

        value = re.sub(
            r"\s+",
            " ",
            value,
        ).strip(" ,")

        return OCRField.from_lines(
            selected,
            value,
        )