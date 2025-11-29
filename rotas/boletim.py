from fastapi import APIRouter

router = APIRouter(
    prefix="/boletim",
    tags=["Boletim"],   
)

# Home
@router.get("/")
async def root():
    return {"msg": "Bem-vindo ao FastAPI!"}