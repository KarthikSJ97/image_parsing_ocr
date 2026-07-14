import re

from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class YearExtractor(BaseExtractor):

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:

        for line in region:

            text = line.text.lower()

            if (
                "birth" in text
                or "year" in text
                or "yob" in text
            ):

                match = re.search(
                    r"(19|20)\d{2}",
                    line.text,
                )

                if match:
                    return OCRField.from_line(
                        line,
                        match.group(),
                    )

        return OCRField.empty()