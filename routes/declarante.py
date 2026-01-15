from fastapi import APIRouter, Depends, Query, status
from schemas.declarante import DeclaranteCreate, DeclaranteResponse, DeclaranteNumerosDeRegistros
from service.declarante import DeclaranteService


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
async def read_declarantes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
):
    return await service.list_declarantes(offset, limit)

@router.get(
    path="/sem-boletim",
    status_code=status.HTTP_200_OK,
    response_model=list[DeclaranteResponse],
    description="busca todos os declarantes sem boletim"    
)
async def declarantes_sem_boletim(
    offset: int = 0,
    limit: int = 10,
):
    return await service.declarantes_sem_boletim(offset, limit)

@router.get(
    path="/ranking",
    status_code=status.HTTP_200_OK,
    response_model=list[DeclaranteNumerosDeRegistros],
    description="busca declarantes que possuem mais boletins registrados"    
)
async def ranking_declarantes(
    offset: int = 0,
    limit: int = 10,
):
    return await service.ranking_declarantes(offset, limit)

@router.get(
    path="/reincidentes/tipo",
    status_code=status.HTTP_200_OK,
    response_model=list[DeclaranteResponse],
    description="busca declarantes por reincidentes"    
)
async def declarantes_reincidentes_por_tipo(
    offset: int = 0,
    limit: int = 10,
):
    return await service.declarantes_reincidentes_por_tipo(offset, limit)

@router.get(
    path="/{id_declarante}",
    response_model=DeclaranteResponse,
    status_code=status.HTTP_200_OK,
    description="busca declarante por id"    
)
async def read_declarante(
    id_declarante: int,
):
    return await service.get_declarante(id_declarante)


@router.put(
    path="/{id_declarante}",
    response_model=DeclaranteResponse,
    status_code=status.HTTP_200_OK,
    description="edita um declarante"    
)
async def update_declarante(
    id_declarante: int,
    declarante: DeclaranteCreate,
):
    return await service.update_declarante(id_declarante, declarante)


@router.delete(
    path="/{id_declarante}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="deleta um declarante"    
)
async def delete_declarante(id_declarante: int):
    return await service.delete_declarante(id_declarante)


