from models.extraction_result import ExtractionResult
from models.ocr_document import OCRDocument

from parsers.base_parser import BaseParser


class AadhaarParser(BaseParser):

    def parse(self, document: OCRDocument) -> ExtractionResult:
        return ExtractionResult(
            document_type="aadhaar",
            confidence=1.0,
            fields={},
            raw_text=document.full_text,
        )