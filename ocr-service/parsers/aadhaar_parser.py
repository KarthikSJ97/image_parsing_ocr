import re

from models.extraction_result import ExtractionResult
from models.ocr_document import OCRDocument
from models.ocr_region import OCRRegion
from parsers.base_parser import BaseParser


class AadhaarParser(BaseParser):

    def parse(
        self,
        document: OCRDocument,
    ) -> ExtractionResult:

        identity_region = self.get_identity_region(document)

        fields = {
            "name": self.extract_name(identity_region),
            "aadhaar_number": self.extract_aadhaar_number(document),
            "gender": self.extract_gender(identity_region),
            "year_of_birth": self.extract_year_of_birth(identity_region),
        }

        confidence = (
            sum(
                value is not None
                for value in fields.values()
            )
            /
            len(fields)
        )

        return ExtractionResult(
            document_type="aadhaar",
            confidence=confidence,
            fields=fields,
            raw_text=document.full_text,
        )


    ##############################################################
    # REGION
    ##############################################################

    def get_identity_region(
        self,
        document: OCRDocument,
    ) -> OCRRegion:

        lines = document.between(
            "Government of India",
            "Address",
        )

        return OCRRegion(lines)


    ##############################################################
    # NAME
    ##############################################################

    def extract_name(
        self,
        region: OCRRegion,
    ) -> str | None:

        lines = region.lines()

        father_index = None

        for index, line in enumerate(lines):

            text = line.text.lower()

            if (
                "s/o" in text
                or "d/o" in text
                or "w/o" in text
                or "care of" in text
            ):
                father_index = index
                break


        if father_index is None:
            return None


        candidates = lines[:father_index]


        blacklist = {
            "government",
            "india",
            "uidai",
            "aadhaar",
            "unique",
            "identification",
            "authority",
            "enrollment",
            "help",
        }


        for line in reversed(candidates):

            text = line.text.strip()

            if not text:
                continue


            lower = text.lower()


            if any(
                word in lower
                for word in blacklist
            ):
                continue


            if re.search(
                r"\d",
                text,
            ):
                continue


            words = text.split()


            if len(words) < 2:
                continue


            if len(words) > 5:
                continue


            return text


        return None


    ##############################################################
    # GENDER
    ##############################################################

    def extract_gender(
        self,
        region: OCRRegion,
    ) -> str | None:

        line = region.find("male")

        if line:
            if "female" in line.text.lower():
                return "Female"

            return "Male"

        return None


    ##############################################################
    # YEAR OF BIRTH
    ##############################################################

    def extract_year_of_birth(
        self,
        region: OCRRegion,
    ) -> str | None:

        for line in region.lines():

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
                    return match.group()

        return None


    ##############################################################
    # AADHAAR NUMBER
    ##############################################################

    def extract_aadhaar_number(
        self,
        document: OCRDocument,
    ) -> str | None:

        numbers = re.findall(
            r"\b\d{4}\s\d{4}\s\d{4}\b",
            document.full_text,
        )

        for number in numbers:

            if number.startswith("1800"):
                continue

            return number

        return None