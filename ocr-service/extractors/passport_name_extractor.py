from extractors.base_extractor import BaseExtractor
from models.ocr_document import OCRDocument
from models.ocr_field import OCRField


class PassportNameExtractor(BaseExtractor):

    def extract(
        self,
        document: OCRDocument,
    ) -> OCRField:

        lines = document.lines

        collecting = False
        name_lines = []

        for line in lines:

            text = line.text.upper()

            if "GIVEN NAME" in text:
                collecting = True
                continue

            if collecting:

                if "NATIONALITY" in text:
                    break

                if line.text.strip():
                    name_lines.append(line)

        if not name_lines:
            return OCRField.empty()

        return OCRField.from_lines(
            name_lines,
            " ".join(
                line.text.strip()
                for line in name_lines
            ),
        )