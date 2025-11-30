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

@router.post("/", response_model=Declarante, status_code=status.HTTP_201_CREATED)
async def create_declarante(
    declarante: DeclaranteBase,
    session: AsyncSession = Depends(get_session)
):
    return await service.create_declarante(declarante, session)


@router.get("/", response_model=List[Declarante])
async def read_declarantes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: AsyncSession = Depends(get_session)
):
    return await service.list_declarantes(offset, limit, session)


@router.get("/{id_declarante}", response_model=Declarante)
async def read_declarante(id_declarante: int, session: AsyncSession = Depends(get_session)):
    return await service.get_declarante(id_declarante, session)


@router.put("/{id_declarante}", response_model=Declarante)
async def update_declarante(
    id_declarante: int,
    declarante: DeclaranteBase,
    session: AsyncSession = Depends(get_session)
):
    return await service.update_declarante(id_declarante, declarante, session)


@router.delete("/{id_declarante}", status_code=status.HTTP_200_OK)
async def delete_declarante(id_declarante: int, session: AsyncSession = Depends(get_session)):
    return await service.delete_declarante(id_declarante, session)

@router.get("/reincidentes/tipo")
async def declarantes_reincidentes_por_tipo(
    session: AsyncSession = Depends(get_session)
):
    return await service.declarantes_reincidentes_por_tipo(session)


@router.get("/sem-boletim")
async def declarantes_sem_boletim(
    session: AsyncSession = Depends(get_session)
):
    return await service.declarantes_sem_boletim(session)


@router.get("/ranking")
async def ranking_declarantes(
    session: AsyncSession = Depends(get_session)
):
    return await service.ranking_declarantes(session)
