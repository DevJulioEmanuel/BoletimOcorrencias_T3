from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from enum import Enum
from models.declarante_boletim import DeclaranteBoletim

class TipoEnvolvimento(Enum):
    DECLARANTE = "Declarante"
    VITIMA = "Vítima"
    AUTOR = "Autor_Crime"
    SUSPEITO = "Suspeito"
    TESTEMUNHA = "Testemunha"
    OUTRO = "Outro"

class Declarante(SQLModel, table=True):
    __tablename__ = "declarante"

    id_declarante: int | None = Field(default=None, primary_key=True)
    nome: str
    cpf: str
    data_nascimento: date
    endereco: str
    tipo_envolvimento: TipoEnvolvimento

    # declarante_boletim: list["DeclaranteBoletim"] = Relationship(back_populates="declarante")

    boletins: list["BoletimOcorrencia"] = Relationship(
        back_populates="declarantes",
        link_model=DeclaranteBoletim,
    )

