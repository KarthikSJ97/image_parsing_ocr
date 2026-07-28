from parsers.base_parser import BaseParser

from extractors.aadhaar_number_extractor import AadhaarNumberExtractor
from extractors.aadhaar_address_extractor import AadhaarAddressExtractor
from extractors.aadhaar_gender_extractor import AadhaarGenderExtractor
from extractors.aadhaar_name_extractor import AadhaarNameExtractor
from extractors.aadhaar_dob_extractor import AadhaarDOBExtractor

from configs.aadhaar import REGIONS


class AadhaarParser(BaseParser):

    REGIONS = REGIONS

    def extract(self):

        identity = self.regions["identity"]
        demographic = self.regions["demographic"]

        name = AadhaarNameExtractor().extract(identity)

        if name.value is None:
            name = AadhaarNameExtractor().extract(demographic)

        gender = AadhaarGenderExtractor().extract(identity)

        if gender.value is None:
            gender = AadhaarGenderExtractor().extract(demographic)

        year = AadhaarDOBExtractor().extract(identity)

        if year.value is None:
            year = AadhaarDOBExtractor().extract(demographic)

        address = AadhaarAddressExtractor().extract(
            demographic,
            person_name=name.value,
        )

        return {
            "aadhaar_number": AadhaarNumberExtractor().extract(
                self.document,
            ),
            "name": name,
            "gender": gender,
            "year_of_birth": year,
            "address": address,
        }