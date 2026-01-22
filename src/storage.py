import uuid
from src.schemas import Invoice
from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class VectorStorage:
    def __init__(self, qdrant: AsyncQdrantClient, openai_client: AsyncOpenAI):
        self.qdrant = qdrant
        self.openai_client = openai_client

    async def ensure_collection(self):
        ensure = await self.qdrant.collection_exists("invoices")

        if not ensure:
            await self.qdrant.create_collection(
                collection_name="invoices",
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )

    async def add_invoice(self, invoice: Invoice, raw_text: str):
        response = await self.openai_client.embeddings.create(
            input=raw_text, model="text-embedding-3-small"
        )
        embedding = response.data[0].embedding

        await self.qdrant.upsert(
            collection_name="invoices",
            points=[
                PointStruct(
                    id=str(uuid.uuid4()), vector=embedding, payload=invoice.model_dump()
                )
            ],
        )
        print("✅ Zapisano fakturę w Qdrant!")
