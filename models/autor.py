from beanie import Document

class Autor(Document):
    nome: str
    matricula: str
    posto: str
    lotacao: str

    class Settings:
        name = "autores"