from __future__ import annotations

from pathlib import Path
from threading import Lock
from typing import Any

from loguru import logger
from paddleocr import PaddleOCR

from config import settings


class PaddleEngine:
    """
    Singleton wrapper around PaddleOCR.

    Responsibilities:
    - Load the OCR model exactly once.
    - Warm up the model.
    - Provide thread-safe inference.
    """

    _instance: "PaddleEngine | None" = None
    _instance_lock = Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._ocr = None
        self._ready = False
        self._predict_lock = Lock()

        self._initialized = True

    @property
    def ready(self) -> bool:
        return self._ready

    def initialize(self) -> None:
        """
        Loads PaddleOCR into memory.
        Should be called once during FastAPI startup.
        """

        if self._ready:
            return

        logger.info("Loading PaddleOCR model...")

        self._ocr = PaddleOCR(
            lang="en",
            use_doc_orientation_classify=True,
            use_doc_unwarping=True,
            use_textline_orientation=True,
            device="cpu",
        )

        logger.info("PaddleOCR loaded successfully.")

        self._ready = True

    def predict(self, file_path: Path) -> list[Any]:
        """
        Executes OCR inference.

        Thread-safe because PaddleOCR inference is not guaranteed
        to be reentrant across all deployments.
        """

        if not self._ready:
            raise RuntimeError("OCR Engine not initialized")

        with self._predict_lock:
            return list(self._ocr.predict(str(file_path)))