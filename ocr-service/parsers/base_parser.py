from abc import ABC, abstractmethod

from models.ocr_document import OCRDocument
from models.extraction_result import ExtractionResult


class BaseParser(ABC):

    @abstractmethod
    def parse(self, document: OCRDocument) -> ExtractionResult:
        pass