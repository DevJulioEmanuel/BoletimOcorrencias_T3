from sqlmodel import SQLModel, Field
from datetime import date
from models.boletim_ocorrencia import TipoOcorrencia, StatusBoletim

class BoletimOcorrenciaBase(SQLModel):
    data_registro: date
    tipo_ocorrencia: TipoOcorrencia
    descricao: str
    status: StatusBoletim
    autor_id: int
    declarante_ids: list[int] = Field(default_factory=list)