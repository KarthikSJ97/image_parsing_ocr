from extractors.base_extractor import BaseExtractor
from models.ocr_region import OCRRegion
from models.ocr_field import OCRField

import re


class PassportNationalityExtractor(BaseExtractor):

    NATIONALITIES = {
        "INDIAN": "INDIAN",
        "INDIA": "INDIAN",
    }


    def extract(
        self,
        document: OCRRegion,
    ) -> OCRField:


        #
        # 1. Try label based extraction
        #
        label = document.find("Nationality")

        if label is None:
            label = document.find("Nationality/Nationalite")


        if label:

            candidates = []

            #
            # right side candidates
            #
            try:
                candidates.extend(
                    document.right_same_row(label)
                )
            except AttributeError:
                pass


            #
            # below candidates
            #
            try:
                candidates.extend(
                    document.below_aligned(label)
                )
            except AttributeError:
                pass


            result = self._extract_from_candidates(
                candidates
            )

            if result:
                return result


        #
        # 2. Fallback scan all OCR lines
        #
        result = self._extract_from_candidates(
            document.lines
        )

        if result:
            return result


        return OCRField.empty()



    def _extract_from_candidates(
        self,
        lines,
    ):

        for line in lines:

            raw = line.text.upper()


            #
            # Normalize OCR noise
            #
            normalized = (
                raw
                .replace("/", " ")
                .replace("-", " ")
                .replace("|", " ")
            )


            #
            # Remove non alphabet characters
            #
            normalized = re.sub(
                r"[^A-Z ]",
                " ",
                normalized
            )


            normalized = re.sub(
                r"\s+",
                " ",
                normalized
            ).strip()


            #
            # Extract nationality token
            #
            for key, value in self.NATIONALITIES.items():

                if re.search(
                    rf"\b{key}\b",
                    normalized
                ):

                    return OCRField.from_line(
                        line,
                        value,
                    )


        return None