from models.declarante import TipoEnvolvimento

from pydantic import BaseModel

from beanie.odm.fields import PydanticObjectId

class DeclaranteCreate(BaseModel):
    nome: str
    cpf: str
    endereco: str
    tipo_envolvimento: TipoEnvolvimento 

class DeclaranteResponse(DeclaranteCreate):
    id: PydanticObjectId

class DeclaranteNumerosDeRegistros(DeclaranteResponse):
    quantidade_registros: int

