from fastapi import APIRouter

router = APIRouter(
    prefix="/declarante",
    tags=["Declarante"],   
)

# Home
@router.get("/")
async def root():
    return {"msg": "Bem-vindo ao FastAPI!"}