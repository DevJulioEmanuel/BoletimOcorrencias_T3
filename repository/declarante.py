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
        """
        Cria um novo Declarante no banco de dados.

        :param declarante: O esquema de dados do declarante a ser persistido.
        :type declarante: DeclaranteBase
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :raises IntegrityError: Se houver violação de restrição (ex: CPF duplicado).
        :raises SQLAlchemyError: Em caso de qualquer outro erro no banco de dados, realiza rollback e propaga o erro.
        :return: O objeto Declarante recém-criado.
        :rtype: Declarante
        """
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
        """
        Lista declarantes com suporte à paginação.

        :param offset: Deslocamento (posição inicial) da busca.
        :type offset: int
        :param limit: Limite de registros a serem retornados.
        :type limit: int
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de objetos Declarante.
        :rtype: list[Declarante]
        """
        result = await session.execute(
            select(Declarante).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, id_declarante: int, session: AsyncSession):
        """
        Busca um declarante pelo seu ID.

        :param id_declarante: O ID do declarante a ser buscado.
        :type id_declarante: int
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: O objeto Declarante se encontrado, caso contrário None.
        :rtype: Declarante | None
        """
        return await session.get(Declarante, id_declarante)

    async def update(self, db_declarante: Declarante, data: DeclaranteBase, session: AsyncSession):
        """
        Atualiza um declarante existente.

        :param db_declarante: O objeto Declarante do banco de dados a ser atualizado.
        :type db_declarante: Declarante
        :param data: Os dados de atualização do declarante.
        :type data: DeclaranteBase
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :raises IntegrityError: Se houver violação de restrição (ex: CPF duplicado).
        :raises SQLAlchemyError: Em caso de qualquer outro erro de atualização, realiza rollback e propaga o erro.
        :return: O objeto Declarante atualizado.
        :rtype: Declarante
        """
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
        """
        Deleta um declarante do banco de dados.

        :param db_declarante: O objeto Declarante do banco de dados a ser deletado.
        :type db_declarante: Declarante
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :raises IntegrityError: Se houver erro de integridade ao tentar deletar (ex: chave estrangeira).
        :raises SQLAlchemyError: Em caso de qualquer outro erro no banco de dados, realiza rollback e propaga o erro.
        :return: Não retorna nada (None) em caso de sucesso.
        :rtype: None
        """
        await session.delete(db_declarante)

        try:
            await session.commit()
        except (IntegrityError, SQLAlchemyError) as e:
            await session.rollback()
            raise e


    async def declarantes_reincidentes_por_tipo(self, session: AsyncSession):
        """
        Busca declarantes que participaram de mais de um boletim para o mesmo tipo de ocorrência.

        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de tuplas contendo o nome do declarante, o tipo de ocorrência e o total de boletins.
        :rtype: list[tuple[str, str, int]]
        """
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
        """
        Lista declarantes que não estão associados a nenhum boletim de ocorrência (usa OUTER JOIN).

        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de objetos Declarante sem boletins associados.
        :rtype: list[Declarante]
        """
        stmt = (
            select(Declarante)
            .outerjoin(DeclaranteBoletim)
            .where(DeclaranteBoletim.declarante_id == None)
        )

        result = await session.exec(stmt)
        return result.all()

    async def ranking_declarantes(self, session: AsyncSession):
        """
        Calcula o ranking dos declarantes com base no total de boletins de ocorrência em que foram envolvidos.

        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de tuplas (nome do declarante, total de boletins), ordenado de forma decrescente.
        :rtype: list[tuple[str, int]]
        """
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