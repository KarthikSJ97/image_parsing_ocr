from extractors.base_extractor import BaseExtractor
from models.ocr_document import OCRDocument
from models.ocr_field import OCRField


class PassportSurnameExtractor(BaseExtractor):

    def extract(
        self,
        document: OCRDocument,
    ) -> OCRField:

        lines = document.lines

        for i, line in enumerate(lines):

            if "SURNAME" in line.text.upper():

                for candidate in lines[i + 1:]:

                    if candidate.text.strip():

                        return OCRField.from_line(candidate)

        return OCRField.empty()