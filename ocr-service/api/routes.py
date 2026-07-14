import os
import tempfile
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

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".pdf",
}


@router.post("/extract")
async def extract(
    request: Request,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
):
    suffix = Path(file.filename).suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}",
        )

    image_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:
            tmp.write(await file.read())
            image_path = tmp.name

        service = request.app.state.extraction_service

        result = service.extract(
            image_path=image_path,
            document_type=document_type.value,
        )

        return result

    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)


@router.post("/debug/ocr")
async def debug_lines(
    request: Request,
    file: UploadFile = File(...),
):
    suffix = Path(file.filename).suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {suffix}",
        )

    image_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:
            tmp.write(await file.read())
            image_path = tmp.name

        service = request.app.state.extraction_service

        # Use the adapter directly to inspect OCR output.
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
            "lines": sum(len(page.lines) for page in document.pages),
        }

    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)