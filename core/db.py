import sqlite3

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy import event

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()

URL_DATABASE = os.getenv("DATABASE_URL")

engine = create_async_engine(
    URL_DATABASE,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    future=True,
)

@event.listens_for(engine.sync_engine, "connect")
def _set_sqlite_pragma(dbapi_conn, conn_record):
    if isinstance(dbapi_conn, sqlite3.Connection):
        dbapi_conn.execute("PRAGMA journal_mode=WAL;")
        dbapi_conn.execute("PRAGMA synchronous=NORMAL;")
        dbapi_conn.execute("PRAGMA foreign_keys=ON;")

async def get_session():
    async with AsyncSession(engine) as session:
        yield session
