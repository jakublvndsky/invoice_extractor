from fastapi import Request
from src.extractor import InvoiceExtractor
from openai import AsyncOpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from src.config import settings
from contextlib import asynccontextmanager
from src.storage import VectorStorage, AsyncQdrantClient


class InvoiceRequest(BaseModel):
    content: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    app.state.extractor = InvoiceExtractor(openai_client)
    qdrant = AsyncQdrantClient(location=":memory:")
    storage = VectorStorage(qdrant, openai_client)
    app.state.storage = storage
    await storage.ensure_collection()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/extract")
async def extract(request: Request, body: InvoiceRequest):
    response = await request.app.state.extractor.extract_info(body.content)
    await request.app.state.storage.add_invoice(response, body.content)
    return response
