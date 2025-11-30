from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from models.boletim_ocorrencia import BoletimOcorrencia
from schemas.boletim import BoletimOcorrenciaBase
from core.db import get_session
from service.boletim import BoletimService


router = APIRouter(prefix="/boletins", tags=["Boletins"])
service = BoletimService()


@router.post("/", response_model=BoletimOcorrencia, status_code=status.HTTP_201_CREATED)
async def create_boletim(
    boletim: BoletimOcorrenciaBase,
    session: AsyncSession = Depends(get_session)
):
    return await service.create_boletim(boletim, session)


@router.get("/", response_model=List[BoletimOcorrencia])
async def list_boletins(session: AsyncSession = Depends(get_session)):
    return await service.list_boletins(session)


@router.get("/{id_boletim}", response_model=BoletimOcorrencia)
async def get_boletim(id_boletim: int, session: AsyncSession = Depends(get_session)):
    return await service.get_boletim(id_boletim, session)


@router.put("/{id_boletim}", response_model=BoletimOcorrencia)
async def update_boletim(
    id_boletim: int,
    boletim: BoletimOcorrenciaBase,
    session: AsyncSession = Depends(get_session)
):
    return await service.update_boletim(id_boletim, boletim, session)


@router.delete("/{id_boletim}", status_code=status.HTTP_200_OK)
async def delete_boletim(id_boletim: int, session: AsyncSession = Depends(get_session)):
    return await service.delete_boletim(id_boletim, session)
