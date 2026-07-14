from models.ocr_field import OCRField

from pydantic import BaseModel


class ExtractionResult(BaseModel):
    document_type: str
    confidence: float
    fields: dict[str, OCRField]
    raw_text: str