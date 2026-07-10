import re

from models.extraction_result import ExtractionResult
from models.ocr_document import OCRDocument
from parsers.base_parser import BaseParser


class AadhaarParser(BaseParser):

    BLACKLIST = {
        "government",
        "india",
        "uidai",
        "aadhaar",
        "unique",
        "identification",
        "authority",
        "enrollment",
        "male",
        "female",
        "birth",
        "year",
        "address",
        "help",
        "instruction",
        "sample",
        "call",
        "write",
        "email",
        "authenticate",
        "identity",
        "citizenship",
        "care of",
        "c/o",
        "s/o",
        "d/o",
        "w/o",
    }

    def parse(
        self,
        document: OCRDocument,
    ) -> ExtractionResult:

        fields = {
            "name": self.extract_name(document),
            "aadhaar_number": self.extract_aadhaar_number(document),
            "gender": self.extract_gender(document),
            "year_of_birth": self.extract_year_of_birth(document),
        }

        confidence = (
            sum(v is not None for v in fields.values())
            / len(fields)
        )

        return ExtractionResult(
            document_type="aadhaar",
            confidence=confidence,
            fields=fields,
            raw_text=document.full_text,
        )

    ##############################################################
    # NAME
    ##############################################################

    def extract_name(
        self,
        document: OCRDocument,
    ) -> str | None:

        header = document.fuzzy_find(
            "Government of India"
        )

        if header is None:
            return None

        candidates = document.below(header)

        for line in candidates:

            text = line.text.strip()

            if not text:
                continue

            lower = text.lower()

            if any(word in lower for word in self.BLACKLIST):
                continue

            if re.search(r"\d", text):
                continue

            words = text.split()

            if len(words) < 2:
                continue

            if len(words) > 5:
                continue

            if not all(
                word[0].isalpha()
                for word in words
            ):
                continue

            return text

        return None

    ##############################################################
    # GENDER
    ##############################################################

    def extract_gender(
        self,
        document: OCRDocument,
    ) -> str | None:

        for line in document.lines():

            text = line.text.lower()

            if "female" in text:
                return "Female"

            if "male" in text:
                return "Male"

        return None

    ##############################################################
    # YEAR
    ##############################################################

    def extract_year_of_birth(
        self,
        document: OCRDocument,
    ) -> str | None:

        for line in document.lines():

            lower = line.text.lower()

            if (
                "birth" in lower
                or "year" in lower
                or "yob" in lower
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

        candidates = re.findall(
            r"\b\d{4}\s\d{4}\s\d{4}\b",
            document.full_text,
        )

        for number in candidates:

            if number.startswith("1800"):
                continue

            return number

        return None