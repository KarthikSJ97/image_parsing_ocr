import os


class Settings:
    OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "en")

    ENABLE_DOC_UNWARP = (
        os.getenv("ENABLE_DOC_UNWARP", "true").lower() == "true"
    )

    ENABLE_DOC_ORIENTATION = (
        os.getenv("ENABLE_DOC_ORIENTATION", "true").lower() == "true"
    )

    ENABLE_TEXTLINE_ORIENTATION = (
        os.getenv("ENABLE_TEXTLINE_ORIENTATION", "true").lower() == "true"
    )


settings = Settings()