import re
from difflib import SequenceMatcher


class TextUtils:

    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""

        text = text.replace("\n", " ")
        text = text.replace("\t", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip().lower()

    @staticmethod
    def only_digits(text: str) -> str:
        return re.sub(r"\D", "", text)

    @staticmethod
    def only_alphanumeric(text: str) -> str:
        return re.sub(r"[^A-Za-z0-9]", "", text)

    @staticmethod
    def similarity(a: str, b: str) -> float:
        return SequenceMatcher(
            None,
            TextUtils.normalize(a),
            TextUtils.normalize(b),
        ).ratio()

    @staticmethod
    def contains(text: str, keyword: str) -> bool:
        return TextUtils.normalize(keyword) in TextUtils.normalize(text)

    @staticmethod
    def fuzzy_contains(
        text: str,
        keyword: str,
        threshold: float = 0.80,
    ) -> bool:

        text = TextUtils.normalize(text)
        keyword = TextUtils.normalize(keyword)

        if not text or not keyword:
            return False

        # Fast path: exact substring match
        if keyword in text:
            return True

        words = text.split()
        keyword_words = keyword.split()

        window_size = len(keyword_words)

        if window_size == 0:
            return False

        # Compare phrases of the same length
        for i in range(len(words) - window_size + 1):

            candidate = " ".join(
                words[i:i + window_size]
            )

            # Fast path: exact phrase match
            if candidate == keyword:
                return True

            if (
                TextUtils.similarity(
                    candidate,
                    keyword,
                )
                >= threshold
            ):
                return True

        return False

    @staticmethod
    def first_match(
        pattern: str,
        text: str,
    ) -> str | None:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(0)

        return None


    @staticmethod
    def all_matches(
        pattern: str,
        text: str,
    ) -> list[str]:

        return re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )    

    @staticmethod
    def normalize_number(text: str) -> str:

        replacements = {
            "O": "0",
            "o": "0",
            "I": "1",
            "l": "1",
            "|": "1",
            "S": "5",
            "B": "8",
        }

        return "".join(
            replacements.get(c, c)
            for c in text
        )    

    @staticmethod
    def normalize_name(text: str) -> str:

        text = re.sub(r"\s+", " ", text)

        text = text.strip()

        return text.title()    