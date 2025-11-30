import sqlite3
from sqlmodel import SQLModel, Session
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
from models.autor import Autor
from models.declarante import Declarante
from models.BoletimOcorrencia import BoletimOcorrencia
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

@event.listens_for(engine.sync_engine, "connect")
async def _set_sqlite_pragma(dbapi_conn, conn_record):
    async with dbapi_conn.cursor() as cursor:
        if type(dbapi_conn) is sqlite3.Connection:
            await cursor.execute("PRGAMA journal_mode=WAL;")
            await cursor.execute("PRGAMA synchronous=NORMAL;")
            await cursor.execute("PRGAMA foreign_keys=ON;")

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session

