from pydantic import BaseModel

class OCRLine(BaseModel):
    text: str
    confidence: float

class OCRResponse(BaseModel):
    fullText: str
    lines: list[OCRLine]