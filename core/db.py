from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

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

async def get_session():
    async with AsyncSession(engine) as session:
        yield session
