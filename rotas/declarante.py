from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlmodel import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
from models.declarante import Declarante, DeclaranteBase 

from database import get_session
from typing import List, Optional

router = APIRouter(
    prefix="/declarantes",
    tags=["Declarantes"],
)

@router.post("/", response_model=Declarante, status_code=status.HTTP_201_CREATED)
async def create_declarante(declarante: DeclaranteBase, session: AsyncSession = Depends(get_session)):
    novo_declarante = Declarante(**declarante.model_dump())
    session.add(novo_declarante)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Erro de integridade: O CPF do Declarante já pode existir ou outra restrição foi violada."
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados: {e}"
        )
    await session.refresh(novo_declarante)
    return novo_declarante

@router.get("/", response_model=List[Declarante])
async def read_declarantes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: AsyncSession = Depends(get_session)
):
    statement = select(Declarante).offset(offset).limit(limit)
    result = await session.execute(statement)
    declarantes = result.scalars().all()
    return declarantes

@router.get("/{id_declarante}", response_model=Declarante)
async def read_declarante(id_declarante: int, session: AsyncSession = Depends(get_session)):
    declarante = await session.get(Declarante, id_declarante)
    
    if not declarante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Declarante não encontrado")
    
    return declarante

@router.put("/{id_declarante}", response_model=Declarante)
async def update_declarante(
    id_declarante: int,
    declarante: DeclaranteBase,
    session: AsyncSession = Depends(get_session)
):
    db_declarante = await session.get(Declarante, id_declarante)
    if not db_declarante:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Declarante não encontrado"
        )
    
    declarante_data = declarante.model_dump(exclude_unset=True)

    for key, value in declarante_data.items():
        setattr(db_declarante, key, value)

    session.add(db_declarante)

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Erro de integridade (ex: CPF duplicado)."
        )
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no banco de dados ao atualizar: {e}"
        )

    await session.refresh(db_declarante)
    return db_declarante

@router.delete("/{id_declarante}")
async def delete_declarante(id_declarante: int, session: AsyncSession = Depends(get_session)):
    declarante = await session.get(Declarante, id_declarante)
    
    if not declarante:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Declarante não encontrado")
    
    try:
        await session.delete(declarante)
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Error: {e}"
        )
    
    return {"ok": True, "message": f"Declarante com ID {id_declarante} deletado com sucesso."}