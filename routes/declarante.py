from fastapi import APIRouter, status
from schemas.declarante import DeclaranteCreate, DeclaranteResponse, DeclaranteNumerosDeRegistros
from service.declarante import DeclaranteService

from beanie.odm.fields import PydanticObjectId


router = APIRouter(
    prefix="/declarantes",
    tags=["Declarantes"]
)

service = DeclaranteService()

@router.post(
    path="/",
    response_model=DeclaranteResponse,
    status_code=status.HTTP_201_CREATED,
    description="cria um declarante"    
)
async def create_declarante(
    declarante: DeclaranteCreate,
):
    return await service.create_declarante(declarante)


@router.get(
    path="/",
    response_model=list[DeclaranteResponse],
    status_code=status.HTTP_200_OK,
    description="busca todos os declarantes de forma paginada"    
)
async def read_declarantes(skip: int = 0, limit: int = 50):
    return await service.list_declarantes(skip, limit)

@router.get(
    path="/sem-boletim",
    status_code=status.HTTP_200_OK,
    response_model=list[DeclaranteNumerosDeRegistros],
    description="busca todos os declarantes sem boletim"    
)
async def declarantes_sem_boletim(
    skip: int = 0,
    limit: int = 50,
):
    return await service.declarantes_sem_boletim(skip, limit)

@router.get(
    path="/ranking",
    status_code=status.HTTP_200_OK,
    response_model=list[DeclaranteNumerosDeRegistros],
    description="busca declarantes que possuem mais boletins registrados"    
)
async def ranking_declarantes(
    skip: int = 0,
    limit: int = 50,
):
    return await service.ranking_declarantes(skip, limit)

@router.get(
    path="/reincidentes/tipo",
    status_code=status.HTTP_200_OK,
    response_model=list[DeclaranteResponse],
    description="busca declarantes por reincidentes"    
)
async def declarantes_reincidentes_por_tipo(
    skip: int = 0,
    limit: int = 50,
):
    return await service.declarantes_reincidentes_por_tipo(skip, limit)

@router.get(
    path="/{id_declarante}",
    response_model=DeclaranteResponse,
    status_code=status.HTTP_200_OK,
    description="busca declarante por id"    
)
async def read_declarante(
    id_declarante: PydanticObjectId,
):
    return await service.get_declarante(id_declarante)


@router.put(
    path="/{id_declarante}",
    response_model=DeclaranteResponse,
    status_code=status.HTTP_200_OK,
    description="edita um declarante"    
)
async def update_declarante(
    id_declarante: PydanticObjectId,
    declarante: DeclaranteCreate,
):
    return await service.update_declarante(id_declarante, declarante)


@router.delete(
    path="/{id_declarante}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="deleta um declarante"    
)
async def delete_declarante(id_declarante: PydanticObjectId):
    await service.delete_declarante(id_declarante)


