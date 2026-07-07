import tempfile

from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile

from services.ocr_service import OCRService

router = APIRouter()

ocr_service = OCRService()


@router.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(delete=False) as tmp:

        tmp.write(await file.read())

        image_path = tmp.name

    return ocr_service.extract(image_path)