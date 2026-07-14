from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class AddressExtractor:

    BLACKLIST = {
        "address",
        "uidai",
        "aadhaar",
        "government",
        "india",
        "unique identification authority",
        "help",
    }

    STOP_WORDS = {
        "aadhaar - aam aadmi",
    }

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:

        address_lines = []

        for line in region:

            text = line.text.strip()

            if not text:
                continue

            lower = text.lower()

            if any(word in lower for word in self.STOP_WORDS):
                break

            if any(word == lower for word in self.BLACKLIST):
                continue

            address_lines.append(line)

        if not address_lines:
            return OCRField.empty()

        address = ", ".join(
            line.text.strip()
            for line in address_lines
        )

        return OCRField.from_lines(
            address_lines,
            address,
        )