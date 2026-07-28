import logging
import os
import tempfile
import time
import traceback
import uuid
from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)

from models.document_type import DocumentType

router = APIRouter()

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".pdf",
}

MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_upload(file: UploadFile) -> str:
    suffix = Path(file.filename).suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}",
        )

    return suffix


@router.post("/extract")
async def extract(
    request: Request,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
):
    request_id = str(uuid.uuid4())[:8]
    start_time = time.perf_counter()

    logger.info("[%s] New extraction request", request_id)
    logger.info("[%s] Document Type: %s", request_id, document_type.value)
    logger.info("[%s] Filename: %s", request_id, file.filename)

    suffix = validate_upload(file)

    image_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:

            while chunk := await file.read(1024 * 1024):
                tmp.write(chunk)

            image_path = tmp.name

        size = os.path.getsize(image_path)

        logger.info("[%s] Upload Size: %s bytes", request_id, f"{size:,}")

        if size > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail="Maximum upload size exceeded",
            )

        service = request.app.state.extraction_service

        logger.info("[%s] Starting OCR...", request_id)

        service_start = time.perf_counter()

        result = service.extract(
            image_path=image_path,
            document_type=document_type.value,
        )

        logger.info(
            "[%s] OCR completed in %.2fs",
            request_id,
            time.perf_counter() - service_start,
        )

        logger.info(
            "[%s] Total request time %.2fs",
            request_id,
            time.perf_counter() - start_time,
        )

        return result

    except HTTPException:
        raise

    except Exception:
        logger.exception("[%s] OCR extraction failed", request_id)

        raise HTTPException(
            status_code=500,
            detail="OCR extraction failed",
        )

    finally:
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
                logger.info("[%s] Deleted temp file", request_id)
            except OSError:
                logger.warning(
                    "[%s] Failed to delete temp file %s",
                    request_id,
                    image_path,
                )


@router.post("/debug/ocr")
async def debug_lines(
    request: Request,
    file: UploadFile = File(...),
):
    suffix = validate_upload(file)

    image_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:

            while chunk := await file.read(1024 * 1024):
                tmp.write(chunk)

            image_path = tmp.name

        service = request.app.state.extraction_service

        document = service.adapter.extract(image_path)

        print("\n")
        print("=" * 100)
        print("OCR LINES")
        print("=" * 100)

        for page in document.pages:

            print(f"\nPAGE {page.page_number}")
            print("-" * 100)

            for line in page.lines:
                print(
                    f"({line.left:.1f}, {line.top:.1f}) -> "
                    f"({line.right:.1f}, {line.bottom:.1f}) | "
                    f"{line.text}"
                )

        print("=" * 100)

        return {
            "success": True,
            "pages": len(document.pages),
            "lines": sum(
                len(page.lines)
                for page in document.pages
            ),
        }

    finally:
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass