from sqlmodel import SQLModel

class AutorBase(SQLModel):
    nome: str
    matricula: str
    posto: str
    lotacao: str

class AutorRanking(SQLModel):
    nome: str
    total_boletins: int