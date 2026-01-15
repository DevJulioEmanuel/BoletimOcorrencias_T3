from pydantic import BaseModel

class AutorCreate(BaseModel):
    nome: str
    matricula: str
    posto: str
    lotacao: str

class AutorResponse(AutorCreate):
    id: str 
    
    model_config = {"from_attributes": True}