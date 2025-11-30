from sqlmodel import SQLModel
from datetime import date
from models.boletim_ocorrencia import TipoOcorrencia, StatusBoletim

class BoletimOcorrenciaBase(SQLModel):
    data_registro: date
    tipo_ocorrencia: TipoOcorrencia
    descricao: str
    status: StatusBoletim

class BoletimOcorrenciaCreate(BoletimOcorrenciaBase):
    autor_id: int

class BoletimOcorrenciaResponse(BoletimOcorrenciaBase):
    id_boletim: int
