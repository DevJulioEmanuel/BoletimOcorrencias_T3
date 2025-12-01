from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models.autor import Autor
from schemas.autor import AutorBase, AutorRanking
from core.db import get_session
from service.autor import AutorService

router = APIRouter(
    prefix="/autores",
    tags=["Autores"],
)

service = AutorService()


@router.post(
    path="/",
    response_model=Autor,
    status_code=status.HTTP_201_CREATED,
    description="cria um autor"
)
async def create_autor(
    autor: AutorBase,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await service.create_autor(autor, session)
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    path="/",
    response_model=list[Autor],
    status_code=status.HTTP_200_OK,
    description="busca os autores cadastrados"        
)
async def read_autores(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: AsyncSession = Depends(get_session)
):
    return await service.list_autores(offset, limit, session)

@router.get(
    path="/ranking",
    response_model=list[AutorRanking],
    status_code=status.HTTP_200_OK,
    description="busca os autores que mais registraram boletins"
) 
async def ranking_autores_route(
    offset: int = 0, 
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
):
    try:
        return await service.ranking_autores(offset, limit, session)
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao executar a consulta complexa no banco de dados. Detalhe: {e.args[0]}"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro inesperado no servidor."
        )

@router.get(
    path="/{id_autor}",
    response_model=Autor,
    status_code=status.HTTP_200_OK,
    description="busca um autor por id"        
)
async def read_autor(
    id_autor: int,
    session: AsyncSession = Depends(get_session)
):
    autor = await service.get_autor(id_autor, session)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return autor


@router.put(
    path="/{id_autor}",
    response_model=Autor,
    status_code=status.HTTP_200_OK,
    description="edita um autor"    
)
async def update_autor(
    id_autor: int,
    autor: AutorBase,
    session: AsyncSession = Depends(get_session)
):
    try:
        result = await service.update_autor(id_autor, autor, session)
        if not result:
            raise HTTPException(status_code=404, detail="Autor não encontrado")
        return result
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    path="/{id_autor}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="deleta um autor"
)
async def delete_autor(id_autor: int, session: AsyncSession = Depends(get_session)):
    try:
        deleted = await service.delete_autor(id_autor, session)
        if not deleted:
            raise HTTPException(status_code=404, detail="Autor não encontrado")
        return {"ok": True, "message": f"Autor com ID {id_autor} deletado com sucesso."}
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))
    