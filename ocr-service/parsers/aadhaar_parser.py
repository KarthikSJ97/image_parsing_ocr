import re

from models.ocr_region import OCRRegion
from parsers.base_parser import BaseParser


class AadhaarParser(BaseParser):

    def __init__(self):
        super().__init__()

        self.identity_region: OCRRegion | None = None

        self.demographic_region: OCRRegion | None = None

    def extract(self):

        return {
            "name": self.extract_name(),
            "gender": self.extract_gender(),
            "year_of_birth": self.extract_year_of_birth(),
            "aadhaar_number": self.extract_aadhaar_number(),
            "address": self.extract_address(),
        }

    def preprocess(self):

        self.identity_region = self.get_identity_region()

        self.demographic_region = self.get_demographic_region()    


    ##############################################################
    # REGION
    ##############################################################

    def get_identity_region(
        self
    ) -> OCRRegion:

        return self.navigator.region_between(
            "Government of India",
            "Address",
        )


    ##############################################################
    # NAME
    ##############################################################

    def extract_name(
        self
    ) -> str | None:

        lines = self.identity_region.lines()

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

    def extract_gender(self) -> str | None:

        line = self.identity_region.find("male")

        if line:
            if "female" in line.text.lower():
                return "Female"

            return "Male"

        return None


    ##############################################################
    # YEAR OF BIRTH
    ##############################################################

    def extract_year_of_birth(
        self
    ) -> str | None:

        for line in self.identity_region.lines():

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
        self
    ) -> str | None:

        numbers = re.findall(
            r"\b\d{4}\s\d{4}\s\d{4}\b",
            self.document.full_text,
        )

        for number in numbers:

            if number.startswith("1800"):
                continue

            return number

        return None

    def get_demographic_region(self) -> OCRRegion:

        return self.navigator.region_between(
            "Address",
            "Aadhaar - Aam Aadmi",
        )