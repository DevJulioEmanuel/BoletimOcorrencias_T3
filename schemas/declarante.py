from datetime import date
from pydantic import BaseModel
from models.declarante import TipoEnvolvimento

from pydantic import BaseModel
from typing import Optional

class DeclaranteBase(BaseModel):
    nome: str
    cpf: str
    endereco: str
    tipo_envolvimento: str 

class DeclaranteCreate(DeclaranteBase):
    pass

