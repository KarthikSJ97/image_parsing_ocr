from pathlib import Path

from loguru import logger

from core.paddle_engine import PaddleEngine


class OCRService:
    """
    Business layer responsible for:

    - Executing OCR
    - Normalizing PaddleOCR output
    - Returning our own response format
    """

    def __init__(self):
        self.engine = PaddleEngine()

    def extract(self, file_path: Path) -> dict:

        logger.info(f"Running OCR for {file_path}")

        results = self.engine.predict(file_path)

        pages = []

        full_text = []

        for result in results:

            # Official PaddleOCR 3.x API
            data = result.json

            page = {
                "page_index": data.get("page_index"),
                "lines": []
            }

            texts = data.get("rec_texts", [])
            scores = data.get("rec_scores", [])
            boxes = data.get("rec_boxes", [])
            polys = data.get("dt_polys", [])

            for idx, text in enumerate(texts):

                line = {
                    "text": text,
                    "confidence": scores[idx] if idx < len(scores) else None,
                    "bounding_box": boxes[idx] if idx < len(boxes) else None,
                    "polygon": polys[idx] if idx < len(polys) else None,
                }

                page["lines"].append(line)
                full_text.append(text)

            pages.append(page)

        return {
            "pages": pages,
            "full_text": "\n".join(full_text)
        }