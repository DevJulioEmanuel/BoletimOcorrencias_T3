from datetime import date
from models.boletim_ocorrencia import TipoOcorrencia
from pydantic import BaseModel
from models.boletim_ocorrencia import StatusBoletim
from beanie.odm.fields import PydanticObjectId


class BoletimOcorrenciaCreate(BaseModel):
    tipo_ocorrencia: TipoOcorrencia
    status: StatusBoletim
    autor: PydanticObjectId
    declarantes: list[PydanticObjectId] = []

class BoletimOcorrenciaResponse(BaseModel):
    _id: PydanticObjectId
    data_registro: date
    tipo_ocorrencia: str
    status: str

class BoletimOcorrenciaResponseMultiplosDeclarantes(BoletimOcorrenciaResponse):
    total_declarantes: int

    
    class Config:
        from_attributes = True