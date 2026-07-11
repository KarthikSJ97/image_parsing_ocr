import re

from pydantic import BaseModel

from models.ocr_line import OCRLine
from models.ocr_page import OCRPage
from utils.text_utils import TextUtils
from models.ocr_region import OCRRegion

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

    def find_page(
        self,
        line: OCRLine,
    ) -> OCRPage | None:

        for page in self.pages:

            if line in page.lines:
                return page

        return None


    def nearest_below(
        self,
        line: OCRLine,
    ) -> OCRLine | None:

        page = self.find_page(line)

        if page is None:
            return None

        return page.nearest_below(line)


    def below(
        self,
        line: OCRLine,
    ) -> list[OCRLine]:

        page = self.find_page(line)

        if page is None:
            return []

        return page.below(line)    

    def region_between(
        self,
        start: str,
        end: str,
    ) -> OCRRegion:

        return OCRRegion(
            self.between(
                start,
                end,
            )
        )    