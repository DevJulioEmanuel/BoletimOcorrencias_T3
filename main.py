from fastapi import FastAPI

from routes import autor, boletim, declarante

app = FastAPI()

app.include_router(autor.router)
app.include_router(boletim.router)
app.include_router(declarante.router)
