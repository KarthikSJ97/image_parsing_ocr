from parsers.base_parser import BaseParser

from extractors.passport_number_extractor import PassportNumberExtractor
from extractors.passport_name_extractor import PassportNameExtractor
from extractors.passport_surname_extractor import PassportSurnameExtractor
from extractors.passport_nationality_extractor import PassportNationalityExtractor
from extractors.passport_dob_extractor import PassportDOBExtractor
from extractors.passport_expiry_date_extractor import PassportExpiryDateExtractor

from configs.passport import REGIONS

class PassportParser(BaseParser):

    REGIONS = REGIONS

    def extract(self):
        identity = self.regions["identity"]

        return {
            "passport_number": PassportNumberExtractor().extract(identity),
            "name": PassportNameExtractor().extract(identity),
            "surname": PassportSurnameExtractor().extract(identity),
            "nationality": PassportNationalityExtractor().extract(identity),
            "date_of_birth": PassportDOBExtractor().extract(identity),
            "expiry_date": PassportExpiryDateExtractor().extract(identity),
        }