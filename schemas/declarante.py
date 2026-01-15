from pydantic import BaseModel
from models.declarante import TipoEnvolvimento

from pydantic import BaseModel

class DeclaranteCreate(BaseModel):
    nome: str
    cpf: str
    endereco: str
    tipo_envolvimento: TipoEnvolvimento 

class DeclaranteResponse(DeclaranteCreate):
    id: str

class DeclaranteNumerosDeRegistros(DeclaranteResponse):
    quantidade_registros: int

