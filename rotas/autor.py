from fastapi import APIRouter

router = APIRouter(
    prefix="/autor",
    tags=["Autor"],   
)

# Home
@router.get("/")
async def root():
    return {"msg": "Bem-vindo ao FastAPI!"}