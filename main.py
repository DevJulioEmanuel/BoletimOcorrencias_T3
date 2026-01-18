from contextlib import asynccontextmanager
from fastapi import FastAPI

from config.database import init_db
from routes import autor, boletim, declarante


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(autor.router)
app.include_router(boletim.router)
app.include_router(declarante.router)
