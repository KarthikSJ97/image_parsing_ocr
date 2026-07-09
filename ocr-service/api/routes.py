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

        return result.model_dump()

    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)