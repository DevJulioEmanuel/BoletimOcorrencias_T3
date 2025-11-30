from sqlmodel.ext.asyncio.session import AsyncSession
from repository.boletim import BoletimRepository


class BoletimService:

    def __init__(self, repo: BoletimRepository):
        self.repo = repo

    async def listar_completos(self, session: AsyncSession):
        return await self.repo.listar_boletins_completos(session)

    async def boletins_com_mais_de_um_declarante(self, session: AsyncSession):
        return await self.repo.boletins_com_mais_de_um_declarante(session)

    async def boletins_por_posto(self, posto: str, session: AsyncSession):
        return await self.repo.boletins_por_posto(posto, session)

    async def boletins_abertos_por_lotacao_com_multiplos_declarantes(self, lotacao: str, session: AsyncSession):
        return await self.repo.boletins_abertos_por_lotacao_com_multiplos_declarantes(lotacao, session)
