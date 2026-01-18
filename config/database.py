import os
from pymongo import AsyncMongoClient
from beanie import init_beanie
from dotenv import load_dotenv

from models import Autor, Declarante, BoletimOcorrencia

load_dotenv()

client: AsyncMongoClient | None = None

async def init_db():
    global client
    client = AsyncMongoClient(os.getenv("MONGODB_URL"))
    db_name = os.getenv("DB_NAME")

    await init_beanie(
        database=client[db_name],
        document_models=[
            Autor,
            Declarante,
            BoletimOcorrencia
        ]
    )
