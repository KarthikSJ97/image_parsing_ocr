import re

from models.document_type import DocumentType
from models.extraction_result import ExtractionResult
from models.ocr_document import OCRDocument
from parsers.base_parser import BaseParser
from schemas.aadhaar_schema import AadhaarSchema


class AadhaarParser(BaseParser):

    AADHAAR_KEYWORDS = [
        "aadhaar",
        "government of india",
        "unique identification authority",
        "uidai",
    ]

    AADHAAR_NUMBER_REGEX = r"\d{4}\s?\d{4}\s?\d{4}"

    DOB_REGEX = r"\d{2}[/-]\d{2}[/-]\d{4}"

    YOB_REGEX = r"(?:year\s*of\s*birth|yob)\D*(\d{4})"

    def parse(self, document: OCRDocument) -> ExtractionResult:

        schema = AadhaarSchema()

        if self.is_aadhaar(document):
            schema.aadhaar_number = self.extract_aadhaar_number(document)
            schema.name = self.extract_name(document)
            schema.dob = self.extract_dob(document)
            schema.yob = self.extract_yob(document)
            schema.gender = self.extract_gender(document)
            schema.address = self.extract_address(document)

        return ExtractionResult(
            document_type=DocumentType.AADHAAR.value,
            confidence=document.average_confidence,
            fields=schema.model_dump(exclude_none=True),
            raw_text=document.full_text,
        )

    def is_aadhaar(self, document: OCRDocument) -> bool:

        score = 0

        for keyword in self.AADHAAR_KEYWORDS:
            if document.fuzzy_find(keyword):
                score += 1

        return score >= 2

    def extract_aadhaar_number(
        self,
        document: OCRDocument,
    ) -> str | None:

        matches = document.regex(self.AADHAAR_NUMBER_REGEX)

        if not matches:
            return None

        match = re.search(
            self.AADHAAR_NUMBER_REGEX,
            matches[0].text,
        )

        return match.group(0) if match else None

    def extract_dob(
        self,
        document: OCRDocument,
    ) -> str | None:

        matches = document.regex(self.DOB_REGEX)

        if not matches:
            return None

        match = re.search(
            self.DOB_REGEX,
            matches[0].text,
        )

        return match.group(0) if match else None

    def extract_yob(
        self,
        document: OCRDocument,
    ) -> str | None:

        match = re.search(
            self.YOB_REGEX,
            document.full_text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        return None

    def extract_gender(
        self,
        document: OCRDocument,
    ) -> str | None:

        for gender in [
            "Male",
            "Female",
            "Transgender",
        ]:

            if document.find(gender):
                return gender

        return None

    def extract_name(
        self,
        document: OCRDocument,
    ) -> str | None:
        return None

    def extract_address(
        self,
        document: OCRDocument,
    ) -> str | None:
        return None