from sqlmodel import SQLModel, Field, Relationship

class DeclaranteBoletim(SQLModel, table=True):
    __tablename__ = 'declaranteboletim'
    declarante_id: int = Field(foreign_key="declarante.id_declarante", primary_key = True)
    boletim_id: int = Field(foreign_key="boletimocorrencia.id_boletim", primary_key = True)