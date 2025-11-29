from fastapi import FastAPI, Depends
from datetime import datetime
from sqlmodel import SQLModel, Field, select, Session
from models.autor import Autor
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
