import re
from difflib import SequenceMatcher


class TextUtils:

    @staticmethod
    def normalize(text: str) -> str:
        """
        Lowercase + remove extra whitespace.
        """
        return re.sub(r"\s+", " ", text).strip().lower()

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

        if keyword in text:
            return True

        words = text.split()

        for word in words:
            if TextUtils.similarity(word, keyword) >= threshold:
                return True

        return False