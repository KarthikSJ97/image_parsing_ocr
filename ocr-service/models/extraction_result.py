from typing import Any

from pydantic import BaseModel


class ExtractionResult(BaseModel):
    document_type: str
    confidence: float
    fields: dict[str, Any]
    raw_text: str