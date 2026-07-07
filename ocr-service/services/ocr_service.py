from paddleocr import PaddleOCR

class OCRService:

    def __init__(self):

        self.ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False
        )

    def extract(self, image_path):

        result = self.ocr.predict(image_path)

        lines = []

        full_text = []

        for page in result:

            texts = page.get("rec_texts", [])

            scores = page.get("rec_scores", [])

            for text, score in zip(texts, scores):

                lines.append({
                    "text": text,
                    "confidence": float(score)
                })

                full_text.append(text)

        return {
            "fullText": "\n".join(full_text),
            "lines": lines
        }