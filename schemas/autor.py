from pydantic import BaseModel

class AutorBase(BaseModel):
    nome: str
    matricula: str
    posto: str
    lotacao: str

class AutorResponse(AutorBase):
    id: str 
    
    model_config = {"from_attributes": True}