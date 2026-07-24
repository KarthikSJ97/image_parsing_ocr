import re

from extractors.base_extractor import BaseExtractor
from models.ocr_document import OCRDocument
from models.ocr_region import OCRRegion
from models.ocr_line import OCRLine
from models.ocr_field import OCRField


class NameExtractor(BaseExtractor):

    BLACKLIST = {
        "government",
        "india",
        "uidai",
        "aadhaar",
        "unique",
        "identification",
        "authority",
        "enrollment",
        "help",
    }

    RELATIONSHIP_MARKERS = (
        "s/o",
        "d/o",
        "w/o",
        "c/o",
        "care of",
    )

    def extract(
        self,
        source: OCRDocument | OCRRegion,
    ) -> str | None:

        if isinstance(source, OCRDocument):
            lines = source.lines
        else:
            lines = source.lines

        father_index = None

        for index, line in enumerate(lines):

            text = line.text.lower()

            if any(
                marker in text
                for marker in self.RELATIONSHIP_MARKERS
            ):
                father_index = index
                break

        if father_index is None:
            return OCRField.empty()

        candidates = lines[:father_index]

        for line in reversed(candidates):

            text = line.text.strip()

            if not text:
                continue

            lower = text.lower()

            if any(
                word in lower
                for word in self.BLACKLIST
            ):
                continue

            if re.search(r"\d", text):
                continue

            words = text.split()

            if len(words) < 2:
                continue

            if len(words) > 5:
                continue

            return OCRField.from_line(
                line,
                text,
            )

        return OCRField.empty()