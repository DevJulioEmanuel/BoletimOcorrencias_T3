from sqlmodel import SQLModel

class AutorBase(SQLModel):
    nome: str
    matricula: str
    posto: str
    lotacao: str

class AutorCreate(AutorBase):
    pass

class AutorResponse(AutorBase):
    id_autor: int
