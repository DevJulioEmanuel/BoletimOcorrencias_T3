from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from models.autor import Autor
from schemas.autor import AutorBase
from core.db import get_session
from typing import List
from service.autor import AutorService

router = APIRouter(
    prefix="/autores",
    tags=["Autores"],
)

service = AutorService()


@router.post("/", response_model=Autor, status_code=status.HTTP_201_CREATED)
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


@router.get("/", response_model=List[Autor])
async def read_autores(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: AsyncSession = Depends(get_session)
):
    return await service.list_autores(offset, limit, session)


@router.get("/autor/{id_autor}", response_model=Autor)
async def read_autor(id_autor: int, session: AsyncSession = Depends(get_session)):
    autor = await service.get_autor(id_autor, session)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return autor


@router.put("/{id_autor}", response_model=Autor)
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


@router.delete("/{id_autor}")
async def delete_autor(id_autor: int, session: AsyncSession = Depends(get_session)):
    try:
        deleted = await service.delete_autor(id_autor, session)
        if not deleted:
            raise HTTPException(status_code=404, detail="Autor não encontrado")
        return {"ok": True, "message": f"Autor com ID {id_autor} deletado com sucesso."}
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))
