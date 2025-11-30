from sqlmodel.ext.asyncio.session import AsyncSession
from repository.boletim import BoletimRepository
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from schemas.boletim import BoletimOcorrenciaBase
from sqlmodel.ext.asyncio.session import AsyncSession

from repository.boletim import BoletimRepository


class BoletimService:

    def __init__(self):
        self.repo = BoletimRepository()

    async def create_boletim(self, boletim: BoletimOcorrenciaBase, session: AsyncSession):
        try:
            return await self.repo.create(boletim, session)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar boletim: {e}"
            )

    async def list_boletins(self, offset: int, limit: int,session: AsyncSession):
        return await self.repo.list_all(offset, limit, session)

    async def get_boletim(self, id_boletim: int, session: AsyncSession):
        boletim = await self.repo.get_by_id(id_boletim, session)

        if not boletim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boletim não encontrado"
            )

        return boletim

    async def update_boletim(self, id_boletim: int, boletim: BoletimOcorrenciaBase, session: AsyncSession):
        db_boletim = await self.repo.get_by_id(id_boletim, session)

        if not db_boletim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boletim não encontrado"
            )

        try:
            return await self.repo.update(db_boletim, boletim, session)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar boletim: {e}"
            )

    async def delete_boletim(self, id_boletim: int, session: AsyncSession):
        db_boletim = await self.repo.get_by_id(id_boletim, session)

        if not db_boletim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boletim não encontrado"
            )

        try:
            await self.repo.delete(db_boletim, session)
            return {"ok": True, "message": f"Boletim ID {id_boletim} deletado com sucesso."}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao deletar boletim: {e}"
            )


    async def listar_completos(self, session: AsyncSession):
        return await self.repo.listar_boletins_completos(session)

    async def boletins_com_mais_de_um_declarante(self, session: AsyncSession):
        return await self.repo.boletins_com_mais_de_um_declarante(session)

    async def boletins_por_posto(self, posto: str, session: AsyncSession):
        return await self.repo.boletins_por_posto(posto, session)

    async def boletins_abertos_por_lotacao_com_multiplos_declarantes(self, lotacao: str, session: AsyncSession):
        return await self.repo.boletins_abertos_por_lotacao_com_multiplos_declarantes(lotacao, session)
