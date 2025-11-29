from fastapi import FastAPI, Depends
from datetime import datetime
from sqlmodel import SQLModel, Field, select, Session
<<<<<<< HEAD
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from rotas import autor, boletim, declarante
=======
from models.autor import Autor
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from sqlalchemy.ext.asyncio import AsyncSession
>>>>>>> 7bd3955e8183e4597617766539f388525af70d35

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
<<<<<<< HEAD

app.include_router(autor.router)
app.include_router(boletim.router)
app.include_router(declarante.router)
=======
>>>>>>> 7bd3955e8183e4597617766539f388525af70d35
