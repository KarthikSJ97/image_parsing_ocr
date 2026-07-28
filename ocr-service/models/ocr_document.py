from pydantic import BaseModel

from models.ocr_line import OCRLine
from models.ocr_page import OCRPage
from models.ocr_region import OCRRegion
from utils.text_utils import TextUtils


class OCRDocument(BaseModel):

    pages: list[OCRPage]

    full_text: str

    average_confidence: float

    def lines(self) -> list[OCRLine]:
        result: list[OCRLine] = []

        for page in self.pages:
            result.extend(page.lines)

        return result

    def find(
        self,
        keyword: str,
    ) -> OCRLine | None:

        for page in self.pages:
            line = page.find(keyword)

            if line is not None:
                return line

        return None

    def find_all(
        self,
        keyword: str,
    ) -> list[OCRLine]:

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

    def regex(
        self,
        pattern: str,
    ) -> list[OCRLine]:

        result: list[OCRLine] = []

        for page in self.pages:
            result.extend(page.regex(pattern))

        return result

    def page(
        self,
        page_number: int,
    ) -> OCRPage | None:

        for page in self.pages:
            if page.page_number == page_number:
                return page

        return None

    def after(
        self,
        keyword: str,
        limit: int | None = None,
    ) -> list[OCRLine]:

        lines = self.lines()

        index = self._find_keyword_index(
            lines,
            keyword,
        )

        if index is None:
            return []

        result = lines[index + 1:]

        if limit is not None:
            result = result[:limit]

        return result

    def before(
        self,
        keyword: str,
    ) -> list[OCRLine]:

        lines = self.lines()

        index = self._find_keyword_index(
            lines,
            keyword,
        )

        if index is None:
            return lines

        return lines[:index]

    def between(
        self,
        start: str,
        end: str,
    ) -> list[OCRLine]:

        lines = self.lines()

        start_index = self._find_keyword_index(
            lines,
            start,
        )

        if start_index is None:
            return []

        end_index = self._find_keyword_index(
            lines,
            end,
            start_index + 1,
        )

        if end_index is None:
            end_index = len(lines)

        return lines[start_index + 1:end_index]

    def _find_keyword_index(
        self,
        lines: list[OCRLine],
        keyword: str,
        start_index: int = 0,
        max_window: int = 3,
    ) -> int | None:

        for i in range(start_index, len(lines)):

            for window in range(1, max_window + 1):

                if i + window > len(lines):
                    break

                combined = " ".join(
                    line.text
                    for line in lines[i:i + window]
                )

                if TextUtils.fuzzy_contains(
                    combined,
                    keyword,
                ):
                    return i + window - 1

        return None

    def find_page(
        self,
        line: OCRLine,
    ) -> OCRPage | None:

        for page in self.pages:

            if line in page.lines:
                return page

        return None

    def above(
        self,
        line: OCRLine,
    ) -> list[OCRLine]:

        page = self.find_page(line)

        if page is None:
            return []

        return page.above(line)

    def below(
        self,
        line: OCRLine,
    ) -> list[OCRLine]:

        page = self.find_page(line)

        if page is None:
            return []

        return page.below(line)

    def left_of(
        self,
        line: OCRLine,
    ) -> list[OCRLine]:

        page = self.find_page(line)

        if page is None:
            return []

        return page.left_of(line)

    def right_of(
        self,
        line: OCRLine,
    ) -> list[OCRLine]:

        page = self.find_page(line)

        if page is None:
            return []

        return page.right_of(line)

    def nearest_below(
        self,
        line: OCRLine,
    ) -> OCRLine | None:

        page = self.find_page(line)

        if page is None:
            return None

        return page.nearest_below(line)

    def region_between(
        self,
        start: str,
        end: str,
    ) -> OCRRegion:

        return OCRRegion(
            lines=self.between(
                start,
                end,
            )
        )

    def region_after(
        self,
        keyword: str,
        limit: int | None = None,
    ) -> OCRRegion:

        return OCRRegion(
            lines=self.after(
                keyword,
                limit,
            )
        )

    def region_before(
        self,
        keyword: str,
    ) -> OCRRegion:

        return OCRRegion(
            lines=self.before(
                keyword,
            )
        )

    def first_line(self) -> OCRLine | None:

        lines = self.lines()

        if not lines:
            return None

        return lines[0]

    def last_line(self) -> OCRLine | None:

        lines = self.lines()

        if not lines:
            return None

        return lines[-1]

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def is_empty(self) -> bool:
        return self.page_count == 0

    def contains(
        self,
        keyword: str,
    ) -> bool:

        return self.find(keyword) is not None

    def fuzzy_contains(
        self,
        keyword: str,
        threshold: float = 0.80,
    ) -> bool:

        return self.fuzzy_find(
            keyword,
            threshold,
        ) is not None