from parsers.base_parser import BaseParser

from extractors.driving_license_number_extractor import DrivingLicenseNumberExtractor
from extractors.driving_license_name_extractor import DrivingLicenseNameExtractor
from extractors.driving_license_dob_extractor import DrivingLicenseDOBExtractor
from extractors.driving_license_doi_extractor import DrivingLicenseDOIExtractor

from configs.driving_license import REGIONS


class DrivingLicenseParser(BaseParser):

    REGIONS = REGIONS

    def extract(self):

        identity = self.regions["identity"]

        return {
            "license_number": DrivingLicenseNumberExtractor().extract(identity),
            "name": DrivingLicenseNameExtractor().extract(identity),
            "date_of_birth": DrivingLicenseDOBExtractor().extract(identity),
            "date_of_issue": DrivingLicenseDOIExtractor().extract(identity),
        }