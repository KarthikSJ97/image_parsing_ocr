from enum import Enum


class DocumentType(str, Enum):
    UNKNOWN = "unknown"
    AADHAAR = "aadhaar"
    IRCTC = "irctc"
    FLIGHT = "flight"
    PAN = "pan"
    DRIVING_LICENSE = "driving_license"
    PASSPORT = "passport"