from fastapi import APIRouter, Depends, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from models.declarante import Declarante
from schemas.declarante import DeclaranteBase
from core.db import get_session
from service.declarante import DeclaranteService


router = APIRouter(
    prefix="/declarantes",
    tags=["Declarantes"]
)

service = DeclaranteService()

@router.post(
    path="/",
    response_model=Declarante,
    status_code=status.HTTP_201_CREATED,
    description="cria um declarante"    
)
async def create_declarante(
    declarante: DeclaranteBase,
    session: AsyncSession = Depends(get_session)
):
    return await service.create_declarante(declarante, session)


@router.get(
    path="/",
    response_model=List[Declarante],
    description="busca todos os declarantes de forma paginada"    
)
async def read_declarantes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: AsyncSession = Depends(get_session)
):
    return await service.list_declarantes(offset, limit, session)

@router.get(
    path="/sem-boletim",
    description="busca todos os declarantes sem boletim"    
)
async def declarantes_sem_boletim(
    session: AsyncSession = Depends(get_session)
):
    return await service.declarantes_sem_boletim(session)

@router.get(
    path="/ranking",
    description="busca declarantes que possuem mais boletins registrados"    
)
async def ranking_declarantes(
    session: AsyncSession = Depends(get_session)
):
    return await service.ranking_declarantes(session)

@router.get(
    path="/{id_declarante}",
    response_model=Declarante,
    description="busca declarante por id"    
)
async def read_declarante(
    id_declarante: int,
    session: AsyncSession = Depends(get_session)
):
    return await service.get_declarante(id_declarante, session)


@router.put(
    path="/{id_declarante}",
    response_model=Declarante,
    description="edita um declarante"    
)
async def update_declarante(
    id_declarante: int,
    declarante: DeclaranteBase,
    session: AsyncSession = Depends(get_session)
):
    return await service.update_declarante(id_declarante, declarante, session)


@router.delete(
    path="/{id_declarante}",
    status_code=status.HTTP_200_OK,
    description="deleta um declarante"    
)
async def delete_declarante(id_declarante: int, session: AsyncSession = Depends(get_session)):
    return await service.delete_declarante(id_declarante, session)

@router.get(
    path="/reincidentes/tipo",
    description="busca declarantes por reincidentes"    
)
async def declarantes_reincidentes_por_tipo(
    session: AsyncSession = Depends(get_session)
):
    return await service.declarantes_reincidentes_por_tipo(session)

