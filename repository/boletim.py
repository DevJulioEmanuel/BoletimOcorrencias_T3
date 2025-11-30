from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession
from models.boletim_ocorrencia import BoletimOcorrencia
from schemas.boletim import BoletimOcorrenciaBase
from sqlalchemy.orm import selectinload
from models.boletim_ocorrencia import BoletimOcorrencia, StatusBoletim
from models.autor import Autor
from models.declarante_boletim import DeclaranteBoletim
from models.autor import Autor
from models.declarante import Declarante

class BoletimRepository:

    async def create(self, boletim: BoletimOcorrenciaBase, session: AsyncSession) -> BoletimOcorrencia:
        db_boletim = BoletimOcorrencia(**boletim.model_dump(exclude={'declarante_ids'}))
        session.add(db_boletim)

        try:
            await session.commit()
            await session.refresh(db_boletim)

            if boletim.declarante_ids:
                for declarante_id in boletim.declarante_ids:
                    link = DeclaranteBoletim(
                        boletim_id=db_boletim.id_boletim,
                        declarante_id=declarante_id,
                    )
                    session.add(link)

                await session.commit()

            await session.refresh(db_boletim)

            return db_boletim

        except SQLAlchemyError as e:
            await session.rollback()
            raise e

    async def list_all(self, session: AsyncSession):
        result = await session.execute(
            select(BoletimOcorrencia)
        )
        return result.scalars().all()

    async def get_by_id(self, id_boletim: int, session: AsyncSession):
        return await session.get(BoletimOcorrencia, id_boletim)
    
    from models.declarante import Declarante

    async def update(self, db_boletim: BoletimOcorrencia, boletim: BoletimOcorrenciaBase, session: AsyncSession):
        boletim_data = boletim.model_dump(exclude_unset=True)

        for key, value in boletim_data.items():
            if key == "declarante_ids":
                continue
            setattr(db_boletim, key, value)

        if "declarante_ids" in boletim_data:
            novos_declarantes = []

            for id_declarante in boletim_data["declarante_ids"]:
                result = await session.execute(
                    select(Declarante).where(Declarante.id_declarante == id_declarante)
                )
                declarante = result.scalar_one_or_none()

                if declarante:
                    novos_declarantes.append(declarante)

            await session.run_sync(
                lambda s: setattr(db_boletim, 'declarantes', novos_declarantes)
            )

        session.add(db_boletim)

        try:
            await session.commit()
            await session.refresh(db_boletim)
            return db_boletim
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

    async def delete(self, db_boletim: BoletimOcorrencia, session: AsyncSession):
        await session.delete(db_boletim)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


    async def listar_boletins_completos(self, session: AsyncSession):
        stmt = (
            select(BoletimOcorrencia)
            .options(
                selectinload(BoletimOcorrencia.autor),
                selectinload(BoletimOcorrencia.declarantes),
            )
        )

        result = await session.exec(stmt)
        boletins = result.all()

        return [
            {
                "id_boletim": b.id_boletim,
                "data_registro": b.data_registro,
                "tipo_ocorrencia": b.tipo_ocorrencia.value,
                "status": b.status.value,
                "descricao": b.descricao,
                "autor": b.autor,
                "declarantes": b.declarantes
            }
            for b in boletins
        ]



    async def boletins_com_mais_de_um_declarante(self, session: AsyncSession):
        stmt = (
            select(
                BoletimOcorrencia,
                func.count(DeclaranteBoletim.declarante_id).label("total")
            )
            .join(DeclaranteBoletim)
            .group_by(BoletimOcorrencia.id_boletim)
            .having(func.count(DeclaranteBoletim.declarante_id) > 1)
        )

        result = await session.exec(stmt)
        rows = result.all()

        response = [
            {
                "boletim": r[0].model_dump(),
                "total_declarantes": r[1]
            }
            for r in rows
        ]

        return response


    async def boletins_por_posto(self, posto: str, session: AsyncSession):
        stmt = (
        select(BoletimOcorrencia, Autor)
        .join(BoletimOcorrencia.autor)
        .where(Autor.posto == posto)
        )
        result = await session.exec(stmt)
        return result.all()

async def boletins_abertos_por_lotacao_com_multiplos_declarantes(self, lotacao: str, session: AsyncSession):
    stmt = (
        select(
            BoletimOcorrencia.id_boletim,
            BoletimOcorrencia.data_registro,
            BoletimOcorrencia.tipo_ocorrencia,
            BoletimOcorrencia.descricao,
            BoletimOcorrencia.status,
            Autor.nome,
            Autor.lotacao,
            func.count(DeclaranteBoletim.declarante_id).label("total_declarantes")
        )
        .join(BoletimOcorrencia.autor)
        .join(DeclaranteBoletim)
        .where(
            BoletimOcorrencia.status == StatusBoletim.REGISTRADO,
            Autor.lotacao == lotacao
        )
        .group_by(
            BoletimOcorrencia.id_boletim,
            Autor.id_autor
        )
        .having(func.count(DeclaranteBoletim.declarante_id) > 1)
    )

    result = await session.exec(stmt)
    return result.all()
