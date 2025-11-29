from sqlmodel import SQLModel, Field, Relationship

class Autor(SQLModel, table=True):
    __tablename__ = 'autor'
    id_autor: int | None = Field(default_factory=None, primary_key=True)
    nome: str
    matricula: str
    posto: str
    lotacao: str
    boletimOcorrencia: list["BoletimOcorrencia"] = Relationship(back_populates="autor")