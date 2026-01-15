from datetime import date
from enum import Enum
from beanie import Document


class TipoEnvolvimento(str, Enum):
    DECLARANTE = "Declarante"
    VITIMA = "Vítima"
    AUTOR = "Autor_Crime"
    SUSPEITO = "Suspeito"
    TESTEMUNHA = "Testemunha"
    OUTRO = "Outro"

class Declarante(Document):
    nome: str
    cpf: str
    endereco: str
    tipo_envolvimento: TipoEnvolvimento

    class Settings:
        name = "declarantes"
