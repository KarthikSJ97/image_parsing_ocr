import re

from models.ocr_region import OCRRegion
from parsers.base_parser import BaseParser
from extractors.aadhaar_number_extractor import AadhaarNumberExtractor
from extractors.gender_extractor import GenderExtractor
from extractors.year_extractor import YearExtractor
from extractors.name_extractor import NameExtractor


class AadhaarParser(BaseParser):

    REGIONS = AadhaarConfig.REGIONS

    def extract(self):

        identity = self.regions["identity"]

        return {

            "aadhaar_number":
                AadhaarNumberExtractor.extract(
                    self.document,
                ),

            "name":
                NameExtractor.extract(
                    identity,
                ),

            "gender":
                GenderExtractor.extract(
                    identity,
                ),

            "year_of_birth":
                YearExtractor.extract(
                    identity,
                ),

            "address":
                AddressExtractor().extract(
                    self.demographic_region,
                ),
        }