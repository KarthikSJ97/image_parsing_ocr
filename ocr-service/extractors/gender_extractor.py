from models.ocr_field import OCRField
from models.ocr_region import OCRRegion


class GenderExtractor(BaseExtractor):

    def extract(
        self,
        region: OCRRegion,
    ) -> OCRField:

        line = region.find("male")

        if line:
            if "female" in line.text.lower():
                return OCRField.from_line(
                    line,
                    "Female",
                )

            return OCRField.from_line(
                line,
                "Male",
            )

        return OCRField.empty()