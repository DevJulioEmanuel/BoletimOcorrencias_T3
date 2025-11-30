from sqlmodel.ext.asyncio.session import AsyncSession
from repository.autor import AutorRepository
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas.autor import AutorBase, AutorRanking


class AutorService:

    def __init__(self):
        self.repo = AutorRepository()

    async def create_autor(self, autor: AutorBase, session: AsyncSession):
        try:
            return await self.repo.create(autor, session)
        except IntegrityError:
            raise IntegrityError("Matrícula ou ID do Autor já existem.", None, None)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Erro no banco de dados: {e}", None, None)

    async def list_autores(self, offset: int, limit: int, session: AsyncSession):
        return await self.repo.list(offset, limit, session)

    async def get_autor(self, id_autor: int, session: AsyncSession):
        return await self.repo.get_by_id(id_autor, session)

    async def update_autor(self, id_autor: int, autor: AutorBase, session: AsyncSession):
        try:
            return await self.repo.update(id_autor, autor, session)
        except IntegrityError:
            raise IntegrityError("Dados violam restrição (ex: matrícula duplicada).", None, None)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Erro ao atualizar: {e}", None, None)

    async def delete_autor(self, id_autor: int, session: AsyncSession):
        try:
            return await self.repo.delete(id_autor, session)
        except IntegrityError as e:
            raise IntegrityError(f"Erro: {e}", None, None)

    async def ranking_autores(self, session: AsyncSession) -> AutorRanking:
        return await self.repo.ranking_autores(session)
