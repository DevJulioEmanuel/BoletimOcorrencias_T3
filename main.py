import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie
from dotenv import load_dotenv

from models import Autor, Declarante, BoletimOcorrencia
from routes import autor, boletim, declarante

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(autor.router)
app.include_router(boletim.router)
app.include_router(declarante.router)