import re

from models.ocr_document import OCRDocument
from models.ocr_field import OCRField


class AadhaarNumberExtractor(BaseExtractor):

    def extract(
        self,
        document: OCRDocument,
    ) -> OCRField:

        for line in document.lines():

            matches = re.findall(
                r"\b\d{4}\s\d{4}\s\d{4}\b",
                line.text,
            )

            for number in matches:

                if number.startswith("1800"):
                    continue

                return OCRField.from_line(
                    line,
                    number,
                )

        return OCRField.empty()