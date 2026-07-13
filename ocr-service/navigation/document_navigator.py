from typing import List
from models.ocr_region import OCRRegion


class DocumentNavigator:

    def __init__(
        self,
        document: OCRDocument,
    ):
        self.document = document

    ####################################################################
    # Basic Search
    ####################################################################

    def find(
        self,
        keyword: str,
    ) -> OCRLine | None:

        return self.document.find(keyword)

    def find_all(
        self,
        keyword: str,
    ) -> list[OCRLine]:

        return self.document.find_all(keyword)

    def fuzzy_find(
        self,
        keyword: str,
        threshold: float = 0.80,
    ) -> OCRLine | None:

        return self.document.fuzzy_find(
            keyword,
            threshold,
        )

    def regex(
        self,
        pattern: str,
    ) -> list[OCRLine]:

        return self.document.regex(pattern)

    def contains(
        self,
        keyword: str,
    ) -> bool:

        return self.document.contains(keyword)

    def fuzzy_contains(
        self,
        keyword: str,
        threshold: float = 0.80,
    ) -> bool:

        return self.document.fuzzy_contains(
            keyword,
            threshold,
        )

    ####################################################################
    # Document Access
    ####################################################################

    def page(
        self,
        page_number: int,
    ) -> OCRPage | None:

        return self.document.page(page_number)

    def lines(
        self,
    ) -> List[OCRLine]:

        return self.document.lines()

    ####################################################################
    # Spatial Navigation
    ####################################################################    

    def nearest_below(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        return self.document.nearest_below(reference)

    def below(
        self,
        reference: OCRLine,
    ) -> list[OCRLine]:

        return self.document.below(reference)    

    def nearest_above(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        return self.document.nearest_above(reference)   

    def nearest_right(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        return self.document.nearest_right(reference)    

    def nearest_left(
        self,
        reference: OCRLine,
    ) -> OCRLine | None:

        return self.document.nearest_left(reference)  

    def text_below(
        self,
        keyword: str,
    ) -> str | None:

        reference = self.find(keyword)

        if reference is None:
            return None

        line = self.nearest_below(reference)

        if line is None:
            return None

        return line.text    

    def text_above(
        self,
        keyword: str,
    ) -> str | None:

        reference = self.find(keyword)

        if reference is None:
            return None

        line = self.nearest_above(reference)

        if line is None:
            return None

        return line.text    

    def text_right_of(
        self,
        keyword: str,
    ) -> str | None:

        reference = self.find(keyword)

        if reference is None:
            return None

        line = self.nearest_right(reference)

        if line is None:
            return None

        return line.text    

    def text_left_of(
        self,
        keyword: str,
    ) -> str | None:

        reference = self.find(keyword)

        if reference is None:
            return None

        line = self.nearest_left(reference)

        if line is None:
            return None

        return line.text    

    def _region(
        self,
        lines: list[OCRLine],
    ) -> OCRRegion:

        return OCRRegion(lines=lines)

    ####################################################################
    # Region Navigation
    ####################################################################    

    def region_after(
        self,
        keyword: str,
        limit: int | None = None,
    ) -> OCRRegion:

        return self._region(
            self.document.after(
                keyword,
                limit,
            )
        )

    def region_before(
        self,
        keyword: str,
    ) -> OCRRegion:

        return self._region(
            self.document.before(
                keyword,
            )
        )    

    def region_between(
        self,
        start: str,
        end: str,
    ) -> OCRRegion:

        return self._region(
            self.document.between(
                start,
                end,
            )
        )    

    def region_below(
        self,
        keyword: str,
    ) -> OCRRegion:

        reference = self.find(keyword)

        if reference is None:
            return OCRRegion(lines=[])

        return self._region(
            self.document.below(reference)
        )    

    def region_above(
        self,
        keyword: str,
    ) -> OCRRegion:

        reference = self.find(keyword)

        if reference is None:
            return OCRRegion(lines=[])

        return self._region(
            self.document.above(reference)
        )    

    def region_left_of(
        self,
        keyword: str,
    ) -> OCRRegion:

        reference = self.find(keyword)

        if reference is None:
            return OCRRegion(lines=[])

        return self._region(
            self.document.left_of(reference)
        )    

    def region_right_of(
        self,
        keyword: str,
    ) -> OCRRegion:

        reference = self.find(keyword)

        if reference is None:
            return OCRRegion(lines=[])

        return self._region(
            self.document.right_of(reference)
        )    

    ####################################################################
    # Text Helpers
    ####################################################################    

    def text_after(
        self,
        keyword: str,
        limit: int | None = None,
    ) -> str:

        return self.region_after(
            keyword,
            limit,
        ).text

    def text_before(
        self,
        keyword: str,
    ) -> str:

        return self.region_before(
            keyword,
        ).text    

    def text_between(
        self,
        start: str,
        end: str,
    ) -> str:

        return self.region_between(
            start,
            end,
        ).text    

    def text_below_region(
        self,
        keyword: str,
    ) -> str:

        return self.region_below(
            keyword,
        ).text    

    def text_above_region(
        self,
        keyword: str,
    ) -> str:

        return self.region_above(
            keyword,
        ).text    

    def text_left_region(
        self,
        keyword: str,
    ) -> str:

        return self.region_left_of(
            keyword,
        ).text    

    def text_right_region(
        self,
        keyword: str,
    ) -> str:

        return self.region_right_of(
            keyword,
        ).text    

    def text_of(
        self,
        keyword: str,
    ) -> str | None:

        line = self.find(keyword)

        if line is None:
            return None

        return line.text    

    def line_of(
        self,
        keyword: str,
    ) -> OCRLine | None:

        return self.find(keyword)    

    ####################################################################
    # Convenience Methods   
    ####################################################################    

    def exists(
        self,
        keyword: str,
    ) -> bool:

        return self.contains(keyword)

    def first_regex(
        self,
        pattern: str,
    ) -> OCRLine | None:

        matches = self.regex(pattern)

        if not matches:
            return None

        return matches[0]    

    def regex_text(
        self,
        pattern: str,
    ) -> str | None:

        line = self.first_regex(pattern)

        if line is None:
            return None

        return line.text    

    def find_one_of(
        self,
        keywords: list[str],
    ) -> OCRLine | None:

        for keyword in keywords:

            line = self.find(keyword)

            if line is not None:
                return line

        return None    

    def text_one_of(
        self,
        keywords: list[str],
    ) -> str | None:

        line = self.find_one_of(keywords)

        if line is None:
            return None

        return line.text    

    def text_below_one_of(
        self,
        keywords: list[str],
    ) -> str | None:

        line = self.find_one_of(keywords)

        if line is None:
            return None

        below = self.nearest_below(line)

        if below is None:
            return None

        return below.text    

    def text_right_of_one_of(
        self,
        keywords: list[str],
    ) -> str | None:

        line = self.find_one_of(keywords)

        if line is None:
            return None

        right = self.nearest_right(line)

        if right is None:
            return None

        return right.text    

    def text_after_one_of(
        self,
        keywords: list[str],
        limit: int | None = None,
    ) -> str:

        for keyword in keywords:

            if self.exists(keyword):
                return self.text_after(
                    keyword,
                    limit,
                )

        return ""    

        