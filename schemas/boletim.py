from datetime import date
from models.autor import Autor
from models.declarante import Declarante
from models.boletim_ocorrencia import TipoOcorrencia, StatusBoletim, BoletimOcorrencia
from pydantic import BaseModel

class BoletimCreate(BaseModel):
    tipo_ocorrencia: TipoOcorrencia
    status: Status
    autor_id: str 
    declarantes_ids: List[str] = []

class BoletimResponse(BaseModel):
    id: str
    data_registro: date
    tipo_ocorrencia: str
    status: str

    
    class Config:
        from_attributes = True