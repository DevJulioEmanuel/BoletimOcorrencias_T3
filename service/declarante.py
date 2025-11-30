from sqlmodel.ext.asyncio.session import AsyncSession
from repository.declarante import DeclaranteRepository
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from repository.declarante import DeclaranteRepository
from schemas.declarante import DeclaranteBase

class DeclaranteService:

    def __init__(self):
        self.repo = DeclaranteRepository()

    async def create_declarante(self, declarante: DeclaranteBase, session: AsyncSession):
        try:
            return await self.repo.create(declarante, session)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade: CPF já existe ou outra restrição foi violada."
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {e}"
            )

    async def list_declarantes(self, offset: int, limit: int, session: AsyncSession):
        return await self.repo.list_all(offset, limit, session)

    async def get_declarante(self, id_declarante: int, session: AsyncSession):
        declarante = await self.repo.get_by_id(id_declarante, session)

        if not declarante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Declarante não encontrado"
            )

        return declarante

    async def update_declarante(self, id_declarante: int, data: DeclaranteBase, session: AsyncSession):
        db_declarante = await self.repo.get_by_id(id_declarante, session)

        if not db_declarante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Declarante não encontrado"
            )

        try:
            return await self.repo.update(db_declarante, data, session)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade (ex: CPF duplicado)."
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar no banco: {e}"
            )

    async def delete_declarante(self, id_declarante: int, session: AsyncSession):
        db_declarante = await self.repo.get_by_id(id_declarante, session)

        if not db_declarante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Declarante não encontrado"
            )

        try:
            await self.repo.delete(db_declarante, session)
            return {"ok": True, "message": f"Declarante com ID {id_declarante} deletado com sucesso."}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao deletar: {e}"
            )

    async def declarantes_reincidentes_por_tipo(self, session: AsyncSession):
        return await self.repo.declarantes_reincidentes_por_tipo(session)

    async def declarantes_sem_boletim(self, session: AsyncSession):
        return await self.repo.declarantes_sem_boletim(session)

    async def ranking_declarantes(self, session: AsyncSession):
        return await self.repo.ranking_declarantes(session)
