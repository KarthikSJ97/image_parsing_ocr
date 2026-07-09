from parsers.aadhaar_parser import AadhaarParser
from parsers.flight_parser import FlightParser
from parsers.irctc_parser import IRCTCParser


class ParserRegistry:

    def __init__(self):
        self.parsers = {
            "aadhaar": AadhaarParser(),
            "irctc": IRCTCParser(),
            "flight": FlightParser(),
        }

    def get(self, document_type: str):
        parser = self.parsers.get(document_type)

        if parser is None:
            raise ValueError(f"Unsupported document type: {document_type}")

        return parser