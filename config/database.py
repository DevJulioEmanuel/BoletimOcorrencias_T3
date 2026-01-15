import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.models import Autor, Declarante, BoletimOcorrencia

async def init_db():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    
    await init_beanie(
        database=client.db_policia,
        document_models=[
            Autor,
            Declarante,
            BoletimOcorrencia
        ]
    )