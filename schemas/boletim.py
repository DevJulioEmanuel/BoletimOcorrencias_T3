from sqlmodel import SQLModel, Field
from datetime import date
from models.autor import Autor
from models.declarante import Declarante
from models.boletim_ocorrencia import TipoOcorrencia, StatusBoletim, BoletimOcorrencia

class BoletimOcorrenciaBase(SQLModel):
    data_registro: date
    tipo_ocorrencia: TipoOcorrencia
    descricao: str
    status: StatusBoletim
    autor_id: int
    declarante_ids: list[int] = Field(default_factory=list)


class BoletimOcorrenciaCompleto(SQLModel):
    id_boletim: int
    data_registro: date
    tipo_ocorrencia: str
    status: str
    descricao: str
    autor: Autor
    declarantes: list[Declarante] = Field(default_factory=list)

class BoletimOcorrenciaPorDeclarantes(SQLModel):
    boletim: BoletimOcorrencia
    total_declarantes: int

class BoletimOcorrenciaResumo(SQLModel):
    id_boletim: int
    data_registro: date
    tipo_ocorrencia: str
    descricao: str
    status: str
    nome_autor: str
    lotacao_autor: str
    total_declarantes: int
