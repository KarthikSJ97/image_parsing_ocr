from parsers.base_parser import BaseParser

from extractors.aadhaar_number_extractor import AadhaarNumberExtractor
from extractors.gender_extractor import GenderExtractor
from extractors.year_extractor import YearExtractor
from extractors.name_extractor import NameExtractor
from extractors.address_extractor import AddressExtractor

from configs.aadhaar import REGIONS


class AadhaarParser(BaseParser):

    REGIONS = REGIONS

    def preprocess(self):
        self.identity_region = self.region("identity")
        self.demographic_region = self.region("demographic")

    def extract(self):

        return {
            "aadhaar_number": AadhaarNumberExtractor().extract(self.document),

            "name": NameExtractor().extract(
                self.identity_region,
            ),

            "gender": GenderExtractor().extract(
                self.identity_region,
            ),

            "year_of_birth": YearExtractor().extract(
                self.identity_region,
            ),

            "address": AddressExtractor().extract(
                self.demographic_region,
            ),
        }