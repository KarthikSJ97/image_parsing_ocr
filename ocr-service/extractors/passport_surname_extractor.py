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

            text = line.text.upper()


            if "SURNAME" in text:

                for candidate in lines[i+1:i+5]:

                    value = candidate.text.strip().upper()


                    if (
                        value.isalpha()
                        and len(value) > 2
                    ):

                        return OCRField.from_line(
                            candidate,
                            value,
                        )


        # fallback:
        # Indian passport surname usually appears near top-left

        for line in lines:

            value = line.text.strip().upper()

            if (
                value.isalpha()
                and len(value) > 3
            ):
                return OCRField.from_line(
                    line,
                    value,
                )


        return OCRField.empty()