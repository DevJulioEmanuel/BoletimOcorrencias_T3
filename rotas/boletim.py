from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from typing import List

from models.BoletimOcorrencia import BoletimOcorrencia, BoletimOcorrenciaBase
from database import get_session

router = APIRouter(prefix="/boletins", tags=["Boletins"])

@router.post("/", response_model=BoletimOcorrencia, status_code=status.HTTP_201_CREATED)
async def create_boletim(
    boletim: BoletimOcorrenciaBase,
    session: AsyncSession = Depends(get_session)
):
    db_boletim = BoletimOcorrencia(**boletim.model_dump())

    session.add(db_boletim)

    try:
        await session.commit()
        await session.refresh(db_boletim)
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar boletim: {e}"
        )

    return db_boletim


@router.get("/", response_model=List[BoletimOcorrencia])
async def list_boletins(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        BoletimOcorrencia.__table__.select()
    )
    return result.scalars().all()


@router.get("/{id_boletim}", response_model=BoletimOcorrencia)
async def get_boletim(id_boletim: int, session: AsyncSession = Depends(get_session)):
    boletim = await session.get(BoletimOcorrencia, id_boletim)

    if not boletim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Boletim não encontrado"
        )

    return boletim

@router.put("/{id_boletim}", response_model=BoletimOcorrencia)
async def update_boletim(
    id_boletim: int,
    boletim: BoletimOcorrenciaBase,
    session: AsyncSession = Depends(get_session)
):
    db_boletim = await session.get(BoletimOcorrencia, id_boletim)

    if not db_boletim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Boletim não encontrado"
        )

    boletim_data = boletim.model_dump(exclude_unset=True)

    for key, value in boletim_data.items():
        setattr(db_boletim, key, value)

    session.add(db_boletim)

    try:
        await session.commit()
        await session.refresh(db_boletim)
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar boletim: {e}"
        )

    return db_boletim


@router.delete("/{id_boletim}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_boletim(id_boletim: int, session: AsyncSession = Depends(get_session)):
    db_boletim = await session.get(BoletimOcorrencia, id_boletim)

    if not db_boletim:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Boletim não encontrado"
        )

    await session.delete(db_boletim)

    try:
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar boletim: {e}"
        )

    return {"ok": True, "message": f"Declarante com ID {id_declarante} deletado com sucesso."}
