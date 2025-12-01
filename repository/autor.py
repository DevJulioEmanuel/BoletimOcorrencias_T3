from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from schemas.autor import AutorBase
from models.autor import Autor
from models.boletim_ocorrencia import BoletimOcorrencia

class AutorRepository:

    async def create(self, autor: AutorBase, session: AsyncSession) -> Autor:
        """
        Cria um novo Autor no banco de dados.

        :param autor: O esquema de dados do autor a ser persistido.
        :type autor: AutorBase
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :raises Exception: Propaga exceções de banco de dados (ex: IntegrityError) após rollback.
        :return: O objeto Autor recém-criado.
        :rtype: Autor
        """
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
        """
        Lista autores com suporte à paginação.

        :param offset: Deslocamento (posição inicial) da busca.
        :type offset: int
        :param limit: Limite de registros a serem retornados.
        :type limit: int
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de objetos Autor.
        :rtype: list[Autor]
        """
        stmt = select(Autor).offset(offset).limit(limit)
        result = await session.exec(stmt)
        return result.all()

    async def get_by_id(self, id_autor: int, session: AsyncSession) -> Autor | None:
        """
        Busca um autor pelo seu ID.

        :param id_autor: O ID do autor a ser buscado.
        :type id_autor: int
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: O objeto Autor se encontrado, caso contrário None.
        :rtype: Autor | None
        """
        return await session.get(Autor, id_autor)

    async def update(self, id_autor: int, autor: AutorBase, session: AsyncSession) -> Autor:
        """
        Atualiza um autor existente pelo seu ID.

        :param id_autor: O ID do autor a ser atualizado.
        :type id_autor: int
        :param autor: Os dados de atualização do autor.
        :type autor: AutorBase
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :raises Exception: Propaga exceções de banco de dados (ex: IntegrityError) após rollback.
        :return: O objeto Autor atualizado ou None se o autor não for encontrado.
        :rtype: Autor | None
        """
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
        """
        Deleta um autor pelo seu ID.

        :param id_autor: O ID do autor a ser deletado.
        :type id_autor: int
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :raises Exception: Propaga exceções de banco de dados (ex: IntegrityError) após rollback.
        :return: True se o autor foi deletado com sucesso, False se o autor não for encontrado.
        :rtype: bool
        """
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


    async def ranking_autores(self, offset:int, limit: int, session: AsyncSession):
        """
        Calcula o ranking dos autores com base no total de boletins de ocorrência que registraram.

        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de tuplas (nome do autor, total de boletins), ordenado de forma decrescente.
        :rtype: list[tuple[str, int]]
        """
        stmt = (
            select(
                Autor.nome,
                func.count(BoletimOcorrencia.id_boletim).label("total_boletins")
            )
            .join(BoletimOcorrencia)
            .group_by(Autor.id_autor)
            .order_by(func.count(BoletimOcorrencia.id_boletim).desc())
            .offset(offset).limit(limit)
        )

        result = await session.exec(stmt)
        return result.all()