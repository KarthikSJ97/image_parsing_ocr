import re

from extractors.base_extractor import BaseExtractor
from models.ocr_document import OCRDocument
from models.ocr_region import OCRRegion


class RegexExtractor(BaseExtractor):

    def __init__(
        self,
        pattern: str,
        flags: int = re.IGNORECASE,
    ):
        self.pattern = pattern
        self.flags = flags

    def extract(
        self,
        source: OCRDocument | OCRRegion,
    ) -> str | None:

        if isinstance(source, OCRDocument):
            text = source.full_text
        else:
            text = source.text()

        match = re.search(
            self.pattern,
            text,
            self.flags,
        )

        if match is None:
            return None

        return match.group()