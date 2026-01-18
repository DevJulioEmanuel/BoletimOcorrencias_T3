from pydantic import BaseModel
from beanie.odm.fields import PydanticObjectId

class AutorCreate(BaseModel):
    nome: str
    matricula: str
    posto: str
    lotacao: str

class AutorResponse(AutorCreate):
    id: PydanticObjectId

class AutorRanking(AutorResponse):
    nome: str
    total_boletins: int