from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from models.autor import Autor
from models.boletim_ocorrencia import BoletimOcorrencia


class AutorRepository:

    async def ranking_autores(self, session: AsyncSession):
        stmt = (
            select(
                Autor.nome,
                func.count(BoletimOcorrencia.id_boletim).label("total_boletins")
            )
            .join(BoletimOcorrencia)
            .group_by(Autor.id_autor)
            .order_by(func.count(BoletimOcorrencia.id_boletim).desc())
        )

        result = await session.exec(stmt)
        return result.all()
