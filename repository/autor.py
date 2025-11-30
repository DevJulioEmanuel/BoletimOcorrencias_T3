from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from schemas.autor import AutorBase
from models.autor import Autor
from models.boletim_ocorrencia import BoletimOcorrencia

class AutorRepository:

    async def create(self, autor: AutorBase, session: AsyncSession) -> Autor:
        novo_autor = Autor(**autor.model_dump())
        session.add(novo_autor)

        try:
            await session.commit()
        except:
            await session.rollback()
            raise
        await session.refresh(novo_autor)
        return novo_autor

    async def list(self, offset: int, limit: int, session: AsyncSession):
        stmt = select(Autor).offset(offset).limit(limit)
        result = await session.exec(stmt)
        return result.all()

    async def get_by_id(self, id_autor: int, session: AsyncSession) -> Autor | None:
        return await session.get(Autor, id_autor)

    async def update(self, id_autor: int, autor: AutorBase, session: AsyncSession) -> Autor:
        db_autor = await session.get(Autor, id_autor)

        if not db_autor:
            return None

        autor_data = autor.model_dump(exclude_unset=True)
        for key, value in autor_data.items():
            setattr(db_autor, key, value)

        session.add(db_autor)
        try:
            await session.commit()
        except:
            await session.rollback()
            raise

        await session.refresh(db_autor)
        return db_autor

    async def delete(self, id_autor: int, session: AsyncSession) -> bool:
        autor = await session.get(Autor, id_autor)
        if not autor:
            return False

        try:
            await session.delete(autor)
            await session.commit()
        except:
            await session.rollback()
            raise

        return True


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
