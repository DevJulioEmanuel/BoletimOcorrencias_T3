from sqlmodel.ext.asyncio.session import AsyncSession
from repository.autor import AutorRepository


class AutorService:

    def __init__(self, repo: AutorRepository):
        self.repo = repo

    async def ranking_autores(self, session: AsyncSession):
        return await self.repo.ranking_autores(session)
