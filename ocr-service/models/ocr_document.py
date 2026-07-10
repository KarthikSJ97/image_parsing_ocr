import re

from pydantic import BaseModel

from models.ocr_line import OCRLine
from models.ocr_page import OCRPage
from utils.text_utils import TextUtils

class OCRDocument(BaseModel):

    pages: list[OCRPage]

    full_text: str

    average_confidence: float

    def lines(self) -> list[OCRLine]:
        """
        Returns all OCR lines across all pages.
        """
        result: list[OCRLine] = []

        for page in self.pages:
            result.extend(page.lines)

        return result

    def find(self, keyword: str) -> OCRLine | None:
        """
        Returns the first matching line across all pages.
        """
        for page in self.pages:
            line = page.find(keyword)

            if line is not None:
                return line

        return None

    def find_all(self, keyword: str) -> list[OCRLine]:
        """
        Returns all matching lines across all pages.
        """
        result: list[OCRLine] = []

        for page in self.pages:
            result.extend(page.find_all(keyword))

        return result

    def fuzzy_find(
        self,
        keyword: str,
        threshold: float = 0.80,
    ) -> OCRLine | None:

        for page in self.pages:
            line = page.fuzzy_find(
                keyword,
                threshold,
            )

            if line:
                return line

        return None

    def regex(self, pattern: str) -> list[OCRLine]:

        result: list[OCRLine] = []

        for page in self.pages:
            result.extend(page.regex(pattern))

        return result

    def page(self, page_number: int) -> OCRPage | None:
        """
        Returns a page by its page number.
        """
        for page in self.pages:
            if page.page_number == page_number:
                return page

        return None

    
    def after(
        self,
        keyword: str,
        limit: int | None = None,
    ) -> list[OCRLine]:

        collecting = False
        result: list[OCRLine] = []

        for line in self.lines():

            if collecting:
                result.append(line)

                if limit is not None and len(result) >= limit:
                    break

                continue

            if TextUtils.fuzzy_contains(
                line.text,
                keyword,
            ):
                collecting = True

        return result

    def before(
        self,
        keyword: str,
    ) -> list[OCRLine]:

        result: list[OCRLine] = []

        for line in self.lines():

            if TextUtils.fuzzy_contains(
                line.text,
                keyword,
            ):
                break

            result.append(line)

        return result

    def between(
        self,
        start: str,
        end: str,
    ) -> list[OCRLine]:

        collecting = False
        result: list[OCRLine] = []

        for line in self.lines():

            if not collecting:

                if TextUtils.fuzzy_contains(
                    line.text,
                    start,
                ):
                    collecting = True

                continue

            if TextUtils.fuzzy_contains(
                line.text,
                end,
            ):
                break

            result.append(line)

        return result