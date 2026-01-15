from fastapi import APIRouter, Depends, status

from models.boletim_ocorrencia import BoletimOcorrencia
from schemas.boletim import BoletimOcorrenciaResponse, BoletimOcorrenciaCreate, BoletimOcorrenciaResponseMultiplosDeclarantes
from service.boletim import BoletimService


router = APIRouter(prefix="/boletins", tags=["Boletins"])
service = BoletimService()


@router.post(
    path="/",
    response_model=BoletimOcorrenciaResponse,
    status_code=status.HTTP_201_CREATED,
    description="cria um boletim de ocorrencia"
)
async def create_boletim(
    boletim: BoletimOcorrenciaCreate,
):
    return await service.create_boletim(boletim)


@router.get(
    path="/",
    response_model=list[BoletimOcorrenciaResponse],
    status_code=status.HTTP_200_OK,
    description="busca todos os boletins de ocorrencia registrados de forma paginada"
)
async def list_boletins(
    offset: int = 0,
    limit: int = 50,
):
    return await service.list_boletins(offset, limit)

@router.get(
    path="/multiplos-declarantes",
    status_code=status.HTTP_200_OK,
    response_model=list[BoletimOcorrenciaResponseMultiplosDeclarantes],
    description="busca boletins de ocorrencia que tem multiplos declarantes"
)
async def boletins_com_mais_de_um_declarante(
    offset: int = 0,
    limit: int = 50,
):
    return await service.boletins_com_mais_de_um_declarante(offset, limit)


@router.get(
    path="/por-posto/{posto}",
    status_code=status.HTTP_200_OK,
    response_model=list[BoletimOcorrenciaResponse],
    description="busca boletins de ocorrencia por posto especifico"    
)
async def boletins_por_posto(
    posto: str,
    offset: int = 0,
    limit: int = 50,
):
    return await service.boletins_por_posto(posto, offset, limit)


@router.get(
    path="/abertos/lotacao/{lotacao}",
    status_code=status.HTTP_200_OK,
    response_model=list[BoletimOcorrenciaResponse],
    description="busca boletins por lotacao especifica"
)
async def boletins_abertos_por_lotacao_com_multiplos_declarantes(
    lotacao: str,
    offset: int = 0,
    limit: int = 50,
):
    return await service.boletins_abertos_por_lotacao_com_multiplos_declarantes(lotacao, offset, limit)


@router.get(
    path="/{id_boletim}",
    status_code=status.HTTP_200_OK,
    response_model=BoletimOcorrenciaResponse,
    description="busca boletim por id"
)
async def get_boletim(
    id_boletim: int,
):
    return await service.get_boletim(id_boletim)


@router.put(
    path="/{id_boletim}",
    status_code=status.HTTP_200_OK,
    response_model=BoletimOcorrencia
)
async def update_boletim(
    id_boletim: int,
    boletim: BoletimOcorrenciaCreate,
):
    return await service.update_boletim(id_boletim, boletim)


@router.delete(
    path="/{id_boletim}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_boletim(
    id_boletim: int,
):
    return await service.delete_boletim(id_boletim)
