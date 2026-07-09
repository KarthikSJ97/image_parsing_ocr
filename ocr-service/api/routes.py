from pathlib import Path
import os
import tempfile

from fastapi import APIRouter, File, UploadFile, HTTPException

from services.ocr_service import OCRService

router = APIRouter()

ocr_service = OCRService()


@router.post("/ocr")
async def extract(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()

    if suffix not in [".png", ".jpg", ".jpeg", ".bmp", ".pdf"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    image_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:
            tmp.write(await file.read())
            image_path = tmp.name

        document = ocr_service.extract(image_path)

        return document.model_dump()

    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)