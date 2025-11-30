from sqlmodel.ext.asyncio.session import AsyncSession
from repository.declarante import DeclaranteRepository


class DeclaranteService:

    def __init__(self, repo: DeclaranteRepository):
        self.repo = repo

    async def declarantes_reincidentes_por_tipo(self, session: AsyncSession):
        return await self.repo.declarantes_reincidentes_por_tipo(session)

    async def declarantes_sem_boletim(self, session: AsyncSession):
        return await self.repo.declarantes_sem_boletim(session)

    async def ranking_declarantes(self, session: AsyncSession):
        return await self.repo.ranking_declarantes(session)
