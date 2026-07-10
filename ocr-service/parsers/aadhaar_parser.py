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
            sum(value is not None for value in fields.values())
            / len(fields)
        )

        return ExtractionResult(
            document_type="aadhaar",
            confidence=confidence,
            fields=fields,
            raw_text=document.full_text,
        )

    def extract_name(
        self,
        document: OCRDocument,
    ) -> str | None:

        candidates = document.between(
            "Government of India",
            "Male",
        )

        if not candidates:
            candidates = document.after(
                "Government of India",
                limit=15,
            )

        best = None
        best_score = -1

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

            score = 0

            if 2 <= len(words) <= 4:
                score += 10

            if all(word[:1].isupper() for word in words):
                score += 5

            score += len(text)

            if score > best_score:
                best_score = score
                best = text

        return best

    def extract_gender(
        self,
        document: OCRDocument,
    ) -> str | None:

        for page in document.pages:

            for line in page.lines:

                text = line.text.lower()

                if "female" in text:
                    return "Female"

                if "male" in text:
                    return "Male"

        return None

    def extract_year_of_birth(
        self,
        document: OCRDocument,
    ) -> str | None:

        for line in document.lines():

            text = line.text

            lower = text.lower()

            if (
                "year" in lower
                or "birth" in lower
                or "yob" in lower
            ):

                match = re.search(
                    r"(19|20)\d{2}",
                    text,
                )

                if match:
                    return match.group()

        return None

    def extract_aadhaar_number(
        self,
        document: OCRDocument,
    ) -> str |None:

        candidates = re.findall(
            r"\b\d{4}\s\d{4}\s\d{4}\b",
            document.full_text,
        )

        if not candidates:
            return None

        for candidate in candidates:

            if candidate.startswith("1800"):
                continue

            return candidate

        return candidates[0]