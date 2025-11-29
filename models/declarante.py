from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import date
from .Declarante_Boletim import DeclaranteBoletim

class TipoEnvolvimento(Enum):
    DECLARANTE = "Declarante"              
    VITIMA = "Vítima"                      
    AUTOR = "Autor_Crime"                        
    SUSPEITO = "Suspeito"                  
    TESTEMUNHA = "Testemunha"              
    CONDUTOR = "Condutor"                  
    PASSAGEIRO = "Passageiro"              
    PEDESTRE = "Pedestre"                  
    REPRESENTANTE_LEGAL = "Representante Legal"  
    PROPRIETARIO = "Proprietário"          
    ACIONANTE = "Acionante"                
    INDICIADO = "Indiciado"                
    SOCORRISTA = "Socorrista"              
    RESPONSAVEL_ESTABELECIMENTO = "Responsável pelo Estabelecimento"
    OUTRO = "Outro"

class Declarante(SQLModel, table=True):
    __tablename__ = 'declarante'
    id_declarante: int | None = Field(default_factory=None, primary_key=True)
    nome: str
    cpf: str
    data_nascimento: date
    endereco: str
    tipo_envolvimento: TipoEnvolvimento
    boletins: list["BoletimOcorrencia"] = Relationship(back_populates="declarantes", link_model=DeclaranteBoletim)