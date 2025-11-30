from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from models.boletim_ocorrencia import BoletimOcorrencia
from schemas.boletim import BoletimOcorrenciaBase
from core.db import get_session
from service.boletim import BoletimService


router = APIRouter(prefix="/boletins", tags=["Boletins"])
service = BoletimService()


@router.post(
    path="/",
    response_model=BoletimOcorrencia,
    status_code=status.HTTP_201_CREATED,
    description="cria um boletim de ocorrencia"
)
async def create_boletim(
    boletim: BoletimOcorrenciaBase,
    session: AsyncSession = Depends(get_session)
):
    return await service.create_boletim(boletim, session)


@router.get(
    path="/",
    response_model=List[BoletimOcorrencia],
    status_code=status.HTTP_200_OK,
    description="busca todos os boletins de ocorrencia registrados de forma paginada"
)
async def list_boletins(
    offset: int,
    limit: int,
    session: AsyncSession = Depends(get_session)
):
    return await service.list_boletins(offset, limit, session)

@router.get(
    path="/completos",
    status_code=status.HTTP_200_OK,
    description="busca boletins de ocorrencia com sua estrutura completa"
)
async def listar_completos(
    session: AsyncSession = Depends(get_session)
):
    return await service.listar_completos(session)


@router.get(
    path="/multiplos-declarantes",
    status_code=status.HTTP_200_OK,
    description="busca boletins de ocorrencia que tem multiplos declarantes"
)
async def boletins_com_mais_de_um_declarante(
    session: AsyncSession = Depends(get_session)
):
    return await service.boletins_com_mais_de_um_declarante(session)


@router.get(
    path="/por-posto/{posto}",
    status_code=status.HTTP_200_OK,
    description="busca boletins de ocorrencia por posto especifico"    
)
async def boletins_por_posto(
    posto: str,
    session: AsyncSession = Depends(get_session)
):
    return await service.boletins_por_posto(posto, session)


@router.get(
    path="/abertos/lotacao/{lotacao}",
    status_code=status.HTTP_200_OK,
    description="busca boletins por lotacao especifica"
)
async def boletins_abertos_por_lotacao_com_multiplos_declarantes(
    lotacao: str,
    session: AsyncSession = Depends(get_session)
):
    return await service.boletins_abertos_por_lotacao_com_multiplos_declarantes(lotacao, session)


@router.get(
    path="/{id_boletim}",
    status_code=status.HTTP_200_OK,
    response_model=BoletimOcorrencia,
    description="busca boletim por id"
)
async def get_boletim(
    id_boletim: int,
    session: AsyncSession = Depends(get_session)
):
    return await service.get_boletim(id_boletim, session)


@router.put(
    path="/{id_boletim}",
    status_code=status.HTTP_200_OK,
    response_model=BoletimOcorrencia
    
)
async def update_boletim(
    id_boletim: int,
    boletim: BoletimOcorrenciaBase,
    session: AsyncSession = Depends(get_session)
):
    return await service.update_boletim(id_boletim, boletim, session)


@router.delete(
    path="/{id_boletim}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_boletim(
    id_boletim: int,
    session: AsyncSession = Depends(get_session)
):
    return await service.delete_boletim(id_boletim, session)
