from abc import ABC, abstractmethod

from models.ocr_document import OCRDocument
from navigation.document_navigator import DocumentNavigator
from models.ocr_region import OCRRegion


class BaseParser(ABC):

    def __init__(self):
        self.document: OCRDocument | None = None
        self.navigator: DocumentNavigator | None = None
        self.regions = getattr(self, "REGIONS", {})
        self.region_cache: dict[str, OCRRegion] = {}

    def parse(
        self,
        document: OCRDocument,
    ) -> dict:

        self.document = document
        self.navigator = DocumentNavigator(document)

        self.preprocess_regions()
        self.preprocess()

        result = self.extract()

        result = self.postprocess(result)

        self.validate(result)

        return result

    def preprocess(self):
        """
        Override if required.
        """
        pass

    def preprocess_regions(self):

        for name, config in self.REGIONS.items():

            self.region_cache[name] = self.navigator.region_between(
                config["start"],
                config["end"],
            )    

    @abstractmethod
    def extract(self) -> dict:
        pass

    def postprocess(
        self,
        result: dict,
    ) -> dict:
        return result

    def validate(
        self,
        result: dict,
    ):
        pass

    ###########################################################
    # Navigation Helpers
    ###########################################################

    def find(self, keyword: str):
        return self.navigator.find(keyword)

    def find_all(self, keyword: str):
        return self.navigator.find_all(keyword)

    def contains(self, keyword: str):
        return self.navigator.contains(keyword)

    def exists(self, keyword: str):
        return self.navigator.exists(keyword)

    def fuzzy_find(self, keyword: str):
        return self.navigator.fuzzy_find(keyword)

    def regex(self, pattern: str):
        return self.navigator.regex(pattern)

    def regex_text(self, pattern: str):
        return self.navigator.regex_text(pattern)

    def text_of(self, keyword: str):
        return self.navigator.text_of(keyword)

    def text_below(self, keyword: str):
        return self.navigator.text_below(keyword)

    def text_above(self, keyword: str):
        return self.navigator.text_above(keyword)

    def text_left_of(self, keyword: str):
        return self.navigator.text_left_of(keyword)

    def text_right_of(self, keyword: str):
        return self.navigator.text_right_of(keyword)

    def text_after(
        self,
        keyword: str,
        limit: int | None = None,
    ):
        return self.navigator.text_after(
            keyword,
            limit,
        )

    def text_between(
        self,
        start: str,
        end: str,
    ):
        return self.navigator.text_between(
            start,
            end,
        )    

    def region(self, name: str) -> OCRRegion:
        config = self.REGIONS[name]

        return self.navigator.region_between(
            config.start,
            config.end,
        )

    def region_between(
        self,
        start: str,
        end: str,
    ):
        return self.navigator.region_between(start, end)

    def region_after(
        self,
        keyword: str,
        limit: int | None = None,
    ):
        return self.navigator.region_after(keyword, limit)

    def region_before(
        self,
        keyword: str,
    ):
        return self.navigator.region_before(keyword)

    def region_above(
        self,
        keyword: str,
    ):
        return self.navigator.region_above(keyword)

    def region_below(
        self,
        keyword: str,
    ):
        return self.navigator.region_below(keyword)

    def region_left_of(
        self,
        keyword: str,
    ):
        return self.navigator.region_left_of(keyword)

    def region_right_of(
        self,
        keyword: str,
    ):
        return self.navigator.region_right_of(keyword)    

    def region(self, name: str) -> OCRRegion:
        config = self.REGIONS[name]

        return self.navigator.region_between(
            config["start"],
            config["end"],
        )    