from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from paddleocr import PaddleOCR

import tempfile
import traceback
import os
import pprint

app = FastAPI(title="OCR Service")

ocr = None


@app.on_event("startup")
async def startup():
    global ocr

    print("=" * 80)
    print("Loading PaddleOCR...")
    print("=" * 80)

    ocr = PaddleOCR(
        lang="en",
        use_doc_orientation_classify=True,
        use_doc_unwarping=True,
        use_textline_orientation=True,
    )

    print("=" * 80)
    print("PaddleOCR Loaded Successfully")
    print("=" * 80)


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/debug")
async def debug(file: UploadFile = File(...)):
    image_path = None

    try:
        suffix = Path(file.filename).suffix.lower()

        if suffix not in [".jpg", ".jpeg", ".png", ".bmp", ".pdf"]:
            return {
                "success": False,
                "message": f"Unsupported file type: {suffix}"
            }

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:
            tmp.write(await file.read())
            image_path = tmp.name

        print("=" * 80)
        print(f"Saved uploaded file to: {image_path}")
        print("=" * 80)

        print(f"Original filename : {file.filename}")
        print(f"Temporary file    : {image_path}")

        results = list(ocr.predict(image_path))

        print("=" * 80)
        print("Prediction returned:", type(results))
        print("Number of pages:", len(results))
        print("=" * 80)

        if len(results) == 0:
            print("No OCR results returned.")
            return {
                "success": True,
                "pages": 0
            }

        first = results[0]

        print("=" * 80)
        print("AVAILABLE METHODS")
        print([m for m in dir(first) if not m.startswith("_")])
        print("=" * 80)

        print("=" * 80)
        print("OBJECT TYPE")
        print(type(first))
        print("=" * 80)

        print("KEYS")
        try:
            print(list(first.keys()))
        except Exception as e:
            print(e)

        print("=" * 80)

        print("ITEMS")
        try:
            for key, value in first.items():
                print(f"\n===== {key} =====")
                print(type(value))

                if isinstance(value, list):
                    print(f"Length: {len(value)}")
                    pprint.pprint(value[:3])
                else:
                    pprint.pprint(value)

        except Exception as e:
            print(e)

        print("=" * 80)

        return {
            "success": True,
            "pages": len(results)
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }

    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)