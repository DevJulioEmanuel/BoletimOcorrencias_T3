from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlmodel import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
# Importa o módulo de exceções do SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
from models.autor import Autor, AutorBase
from models.BoletimOcorrencia import BoletimOcorrencia
from database import get_session
from typing import List, Optional

router = APIRouter(
    prefix="/autores",
    tags=["Autores"],
)

@router.post("/", response_model=Autor, status_code=status.HTTP_201_CREATED)
async def create_autor(autor: Autor, session: AsyncSession = Depends(get_session)):
    session.add(autor)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Erro de integridade: Matrícula ou ID do Autor já existem."
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados: {e}"
        )
    await session.refresh(autor)
    return autor

@router.get("/", response_model=List[Autor])
async def read_autores(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: AsyncSession = Depends(get_session)
):
    statement = select(Autor).offset(offset).limit(limit)
    result = await session.execute(statement)
    autores = result.scalars().all()
    return autores

@router.get("/autor/{id_autor}", response_model=Autor)
async def read_autor(id_autor: int, session: AsyncSession = Depends(get_session)):
    autor = await session.get(Autor, id_autor)
    
    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado")
    
    return autor

@router.put("/{id_autor}", response_model=Autor)
async def update_autor(id_autor: int, autor: Autor, session: AsyncSession = Depends(get_session)):
    db_autor = await session.get(Autor, id_autor)
    
    if not db_autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado")

    autor_data = autor.model_dump(exclude_unset=True)
    for key, value in autor_data.items():
        setattr(db_autor, key, value)
    
    session.add(db_autor)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Erro de integridade: Os novos dados violam uma restrição (ex: matrícula duplicada)."
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados ao atualizar: {e}"
        )

    await session.refresh(db_autor)
    return db_autor

@router.delete("/{id_autor}")
async def delete_autor(id_autor: int, session: AsyncSession = Depends(get_session)):
    autor = await session.get(Autor, id_autor)
    
    if not autor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor não encontrado")
    
    try:
        await session.delete(autor)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Error: {e}"
        )
    
    return {"ok": True, "message": f"Autor com ID {id_autor} deletado com sucesso."}