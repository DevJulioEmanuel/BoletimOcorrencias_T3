from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from models.declarante import Declarante
from models.declarante_boletim import DeclaranteBoletim
from models.boletim_ocorrencia import BoletimOcorrencia


class DeclaranteRepository:

    async def declarantes_reincidentes_por_tipo(self, session: AsyncSession):
        stmt = (
            select(
                Declarante.nome,
                BoletimOcorrencia.tipo_ocorrencia,
                func.count(BoletimOcorrencia.id_boletim).label("total")
            )
            .join(DeclaranteBoletim, DeclaranteBoletim.declarante_id == Declarante.id_declarante)
            .join(BoletimOcorrencia, BoletimOcorrencia.id_boletim == DeclaranteBoletim.boletim_id)
            .group_by(Declarante.id_declarante, BoletimOcorrencia.tipo_ocorrencia)
            .having(func.count(BoletimOcorrencia.id_boletim) > 1)
        )

        result = await session.exec(stmt)
        return result.all()

    async def declarantes_sem_boletim(self, session: AsyncSession):
        stmt = (
            select(Declarante)
            .outerjoin(DeclaranteBoletim)
            .where(DeclaranteBoletim.declarante_id == None)
        )

        result = await session.exec(stmt)
        return result.all()

    async def ranking_declarantes(self, session: AsyncSession):
        stmt = (
            select(
                Declarante.nome,
                func.count(DeclaranteBoletim.boletim_id).label("total")
            )
            .join(DeclaranteBoletim)
            .group_by(Declarante.id_declarante)
            .order_by(func.count(DeclaranteBoletim.boletim_id).desc())
        )

        result = await session.exec(stmt)
        return result.all()
