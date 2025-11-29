from sqlmodel import SQLModel, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
from models.autor import Autor
from models.declarante import Declarante
from models.BoletimOcorrencia import BoletimOcorrencia, DeclaranteBoletim
from models.Declarante_Boletim import DeclaranteBoletim
from dotenv import load_dotenv
import asyncio
import logging
import os

load_dotenv()

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_async_engine(os.getenv("DATABASE_URL"))

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session

#asyncio.run(create_db_and_tables())