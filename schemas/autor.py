from sqlmodel import SQLModel

class AutorBase(SQLModel):
    nome: str
    matricula: str
    posto: str
    lotacao: str
