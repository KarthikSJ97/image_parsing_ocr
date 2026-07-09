from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings.

    Values can be overridden using environment variables.
    Example:
        APP_NAME=Travel OCR
        LOG_LEVEL=DEBUG
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --------------------------------------------------
    # App
    # --------------------------------------------------

    APP_NAME: str = "OCR Service"

    APP_VERSION: str = "1.0.0"

    LOG_LEVEL: str = "INFO"

    # --------------------------------------------------
    # OCR
    # --------------------------------------------------

    USE_GPU: bool = False

    ENABLE_DOC_ORIENTATION: bool = True

    ENABLE_TEXTLINE_ORIENTATION: bool = True

    ENABLE_DOC_UNWARPING: bool = True

    # Future: Local model directory
    MODEL_DIR: Path = Path("./models")

    # --------------------------------------------------
    # Upload
    # --------------------------------------------------

    MAX_UPLOAD_SIZE_MB: int = 20

    UPLOAD_DIR: Path = Path("./uploads")

    # --------------------------------------------------
    # Supported extensions
    # --------------------------------------------------

    SUPPORTED_IMAGE_TYPES: tuple[str, ...] = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".bmp",
        ".tiff",
        ".pdf",
    )


settings = Settings()

# Create upload directory automatically
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)