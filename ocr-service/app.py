from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="OCR Service",
    version="1.0"
)

@app.get("/health")
def health():
    return {
        "status": "UP"
    }

app.include_router(router)