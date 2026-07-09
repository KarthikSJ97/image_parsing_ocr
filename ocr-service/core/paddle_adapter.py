from pathlib import Path

from paddleocr import PaddleOCR

from models.point import Point
from models.ocr_line import OCRLine
from models.ocr_page import OCRPage
from models.ocr_document import OCRDocument
from config import settings


class PaddleAdapter:
    """
    Thin wrapper around PaddleOCR.

    Responsibilities:
    - Initialize PaddleOCR once.
    - Run OCR.
    - Convert PaddleOCR output into our internal OCRDocument model.
    """

    def __init__(self):
        self.ocr = PaddleOCR(
            lang=settings.OCR_LANGUAGE,
            use_doc_orientation_classify=settings.ENABLE_DOC_ORIENTATION,
            use_doc_unwarping=settings.ENABLE_DOC_UNWARP,
            use_textline_orientation=settings.ENABLE_TEXTLINE_ORIENTATION,
        )

    def extract(self, image_path: str) -> OCRDocument:
        results = list(self.ocr.predict(image_path))

        pages = []

        for page_index, result in enumerate(results):

            texts = result.get("rec_texts", [])
            scores = result.get("rec_scores", [])
            polygons = result.get("dt_polys", [])

            lines = []

            for text, score, polygon in zip(texts, scores, polygons):

                points = [
                    Point(
                        x=float(point[0]),
                        y=float(point[1]),
                    )
                    for point in polygon
                ]

                lines.append(
                    OCRLine(
                        text=text,
                        confidence=float(score),
                        polygon=points,
                    )
                )

            pages.append(
                OCRPage(
                    page_number=page_index + 1,
                    lines=lines,
                )
            )

        return OCRDocument(
            pages=pages,
        )