from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routes import router
from core.paddle_adapter import PaddleAdapter
from parsers.parser_registry import ParserRegistry
from services.extraction_service import ExtractionService


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 80)
    print("Loading PaddleOCR...")
    print("=" * 80)

    adapter = PaddleAdapter()
    registry = ParserRegistry()

    app.state.extraction_service = ExtractionService(
        adapter=adapter,
        registry=registry,
    )

    print("=" * 80)
    print("OCR Service Ready")
    print("=" * 80)

    yield

    print("=" * 80)
    print("Shutting down OCR Service")
    print("=" * 80)


app = FastAPI(
    title="OCR Extraction Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }