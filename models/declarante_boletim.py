from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class DeclaranteBoletim(SQLModel, table=True):
    __tablename__ = "declaranteboletim"

    declarante_id: int = Field(foreign_key="declarante.id_declarante", primary_key=True)
    boletim_id: int = Field(foreign_key="boletimocorrencia.id_boletim", primary_key=True)

    declarante: Optional["Declarante"] = Relationship(back_populates="declarante_boletim")
    boletim: Optional["BoletimOcorrencia"] = Relationship(back_populates="boletim_declarantes")