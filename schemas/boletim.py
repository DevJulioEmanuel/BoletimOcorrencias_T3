from datetime import date
from models.boletim_ocorrencia import TipoOcorrencia
from pydantic import BaseModel
from models.boletim_ocorrencia import StatusBoletim
from typing import List

class BoletimOcorrenciaCreate(BaseModel):
    tipo_ocorrencia: TipoOcorrencia
    status: StatusBoletim
    autor_id: str 
    declarantes_ids: List[str] = []

class BoletimOcorrenciaResponse(BaseModel):
    id: str
    data_registro: date
    tipo_ocorrencia: str
    status: str

class BoletimOcorrenciaResponseMultiplosDeclarantes(BoletimOcorrenciaResponse):
    total_declarantes: int

    
    class Config:
        from_attributes = True