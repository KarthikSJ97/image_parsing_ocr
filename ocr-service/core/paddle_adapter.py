from statistics import mean

from paddleocr import PaddleOCR

from config import settings
from models.ocr_document import OCRDocument
from models.ocr_line import OCRLine
from models.ocr_page import OCRPage
from models.point import Point


class PaddleAdapter:

    def __init__(self):
        self.ocr = PaddleOCR(
            lang=settings.OCR_LANGUAGE,
            use_doc_orientation_classify=settings.ENABLE_DOC_ORIENTATION,
            use_doc_unwarping=settings.ENABLE_DOC_UNWARP,
            use_textline_orientation=settings.ENABLE_TEXTLINE_ORIENTATION,
        )

    def extract(self, image_path: str) -> OCRDocument:

        results = list(self.ocr.predict(image_path))

        pages: list[OCRPage] = []

        full_text_parts: list[str] = []

        all_scores: list[float] = []

        for page in results:

            texts = page["rec_texts"]
            scores = page["rec_scores"]
            polys = page["rec_polys"]

            page_lines: list[OCRLine] = []
            page_text_parts: list[str] = []

            for text, score, poly in zip(texts, scores, polys):

                points = [
                    Point(x=float(p[0]), y=float(p[1]))
                    for p in poly
                ]

                xs = [p.x for p in points]
                ys = [p.y for p in points]

                left = min(xs)
                right = max(xs)
                top = min(ys)
                bottom = max(ys)

                line = OCRLine(
                    text=text,
                    confidence=float(score),
                    polygon=points,
                    left=left,
                    top=top,
                    right=right,
                    bottom=bottom,
                    center_x=(left + right) / 2,
                    center_y=(top + bottom) / 2,
                )

                page_lines.append(line)

                page_text_parts.append(text)

                all_scores.append(float(score))

            page_text = "\n".join(page_text_parts)

            full_text_parts.append(page_text)

            width = None
            height = None

            doc_pre = page.get("doc_preprocessor_res") or {}

            shape = doc_pre.get("output_img_shape")

            if shape and len(shape) >= 2:
                height = int(shape[0])
                width = int(shape[1])

            pages.append(
                OCRPage(
                    page_number = page.get("page_index") or (len(pages) + 1),
                    width=width,
                    height=height,
                    text=page_text,
                    lines=page_lines,
                )
            )

        return OCRDocument(
            pages=pages,
            full_text="\n\n".join(full_text_parts),
            average_confidence=mean(all_scores) if all_scores else 0.0,
        )