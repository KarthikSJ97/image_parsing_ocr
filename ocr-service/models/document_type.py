from enum import Enum


class DocumentType(str, Enum):
    AADHAAR = "aadhaar"
    IRCTC = "irctc"
    FLIGHT = "flight"