from parsers.base_parser import BaseParser

from extractors.aadhaar_number_extractor import AadhaarNumberExtractor
from extractors.address_extractor import AddressExtractor
from extractors.gender_extractor import GenderExtractor
from extractors.name_extractor import NameExtractor
from extractors.year_extractor import YearExtractor

from configs.aadhaar import REGIONS


class AadhaarParser(BaseParser):

    REGIONS = REGIONS

    def extract(self):

        identity = self.regions["identity"]
        demographic = self.regions["demographic"]

        name = NameExtractor().extract(identity)

        gender = GenderExtractor().extract(identity)
        if gender.value is None:
            gender = GenderExtractor().extract(demographic)

        year = YearExtractor().extract(identity)
        if year.value is None:
            year = YearExtractor().extract(demographic)

        address = AddressExtractor().extract(
            demographic,
            person_name=name.value,
        )

        return {
            "aadhaar_number": AadhaarNumberExtractor().extract(self.document),
            "name": name,
            "gender": gender,
            "year_of_birth": year,
            "address": address,
        }