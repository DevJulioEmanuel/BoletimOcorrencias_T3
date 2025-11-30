from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from models.declarante import Declarante
from schemas.declarante import DeclaranteBase
from models.declarante_boletim import DeclaranteBoletim
from models.boletim_ocorrencia import BoletimOcorrencia
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

class DeclaranteRepository:

    async def create(self, declarante: DeclaranteBase, session: AsyncSession) -> Declarante:
        novo = Declarante(**declarante.model_dump())
        session.add(novo)

        try:
            await session.commit()
            await session.refresh(novo)
            return novo
        except (IntegrityError, SQLAlchemyError) as e:
            await session.rollback()
            raise e

    async def list_all(self, offset: int, limit: int, session: AsyncSession):
        result = await session.execute(
            select(Declarante).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, id_declarante: int, session: AsyncSession):
        return await session.get(Declarante, id_declarante)

    async def update(self, db_declarante: Declarante, data: DeclaranteBase, session: AsyncSession):
        declarante_data = data.model_dump(exclude_unset=True)

        for key, value in declarante_data.items():
            setattr(db_declarante, key, value)

        session.add(db_declarante)

        try:
            await session.commit()
            await session.refresh(db_declarante)
            return db_declarante
        except (IntegrityError, SQLAlchemyError) as e:
            await session.rollback()
            raise e

    async def delete(self, db_declarante: Declarante, session: AsyncSession):
        await session.delete(db_declarante)

        try:
            await session.commit()
        except (IntegrityError, SQLAlchemyError) as e:
            await session.rollback()
            raise e


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
