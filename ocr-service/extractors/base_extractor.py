from abc import ABC, abstractmethod

from models.ocr_field import OCRField


class BaseExtractor(ABC):

    @abstractmethod
    def extract(self, *args, **kwargs) -> OCRField:
        """
        Extract a field from OCR content.
        """
        pass