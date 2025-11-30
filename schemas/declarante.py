from datetime import date
from sqlmodel import SQLModel
from models.declarante import TipoEnvolvimento

class DeclaranteBase(SQLModel):
    nome: str
    cpf: str
    data_nascimento: date
    endereco: str
    tipo_envolvimento: TipoEnvolvimento

class DeclaranteCreate(DeclaranteBase):
    pass

class DeclaranteResponse(DeclaranteBase):
    id_declarante: int
