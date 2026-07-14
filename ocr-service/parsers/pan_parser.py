from parsers.base_parser import BaseParser

from extractors.pan_number_extractor import PanNumberExtractor
from extractors.pan_name_extractor import PanNameExtractor
from extractors.date_extractor import DateExtractor
from extractors.pan_father_name_extractor import PanFatherNameExtractor

from configs.pan import REGIONS


class PanParser(BaseParser):

    REGIONS = REGIONS

    def extract(self):

        identity = self.regions["identity"]

        name = PanNameExtractor().extract(identity)

        return {
            "pan_number": PanNumberExtractor().extract(
                identity
            ),

            "date_of_birth": DateExtractor().extract(
                identity
            ),

            "name": name,

            "father_name": PanFatherNameExtractor().extract(
                identity,
                person_name=name.value,
            ),
        }