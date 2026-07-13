from abc import ABC, abstractmethod

from models.ocr_document import OCRDocument
from navigation.document_navigator import DocumentNavigator


class BaseParser(ABC):

    def __init__(self):
        self.document: OCRDocument | None = None
        self.navigator: DocumentNavigator | None = None

    def parse(
        self,
        document: OCRDocument,
    ) -> dict:

        self.document = document
        self.navigator = DocumentNavigator(document)

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