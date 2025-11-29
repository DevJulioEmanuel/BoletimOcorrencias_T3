from fastapi import FastAPI, Depends
from datetime import datetime
from sqlmodel import SQLModel, Field, select, Session
from contextlib import asynccontextmanager
from database import create_db_and_tables, get_session
from rotas import autor, boletim, declarante

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(autor.router)
app.include_router(boletim.router)
app.include_router(declarante.router)