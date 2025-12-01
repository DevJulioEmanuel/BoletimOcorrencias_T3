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
        """
        Cria um novo Boletim de Ocorrência e lida com a associação opcional de Declarantes.

        :param boletim: O esquema de dados do boletim, incluindo a lista de IDs de declarantes.
        :type boletim: BoletimOcorrenciaBase
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :raises SQLAlchemyError: Em caso de qualquer erro no banco de dados, realiza rollback e propaga o erro.
        :return: O objeto BoletimOcorrencia recém-criado, incluindo as associações.
        :rtype: BoletimOcorrencia
        """
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

    async def list_all(self, offset: int, limit: int,session: AsyncSession):
        """
        Lista todos os Boletins de Ocorrência com suporte à paginação.

        :param offset: Deslocamento (posição inicial) da busca.
        :type offset: int
        :param limit: Limite de registros a serem retornados.
        :type limit: int
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Um objeto Result contendo os Boletins de Ocorrência.
        :rtype: Result
        """
        stmt = select(BoletimOcorrencia).offset(offset).limit(limit)
        return await session.exec(stmt)

    async def get_by_id(self, id_boletim: int, session: AsyncSession):
        """
        Busca um Boletim de Ocorrência pelo seu ID.

        :param id_boletim: O ID do boletim a ser buscado.
        :type id_boletim: int
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: O objeto BoletimOcorrencia se encontrado, caso contrário None.
        :rtype: BoletimOcorrencia | None
        """
        return await session.get(BoletimOcorrencia, id_boletim)
    
    from models.declarante import Declarante

    async def update(self, db_boletim: BoletimOcorrencia, boletim: BoletimOcorrenciaBase, session: AsyncSession):
        """
        Atualiza um Boletim de Ocorrência existente, incluindo a atualização dos declarantes associados.

        :param db_boletim: O objeto BoletimOcorrencia do banco de dados a ser atualizado.
        :type db_boletim: BoletimOcorrencia
        :param boletim: Os dados de atualização do boletim.
        :type boletim: BoletimOcorrenciaBase
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :raises SQLAlchemyError: Em caso de qualquer erro no banco de dados, realiza rollback e propaga o erro.
        :return: O objeto BoletimOcorrencia atualizado.
        :rtype: BoletimOcorrencia
        """
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

            # Atualiza a relação many-to-many
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
        """
        Deleta um Boletim de Ocorrência do banco de dados.

        :param db_boletim: O objeto BoletimOcorrencia do banco de dados a ser deletado.
        :type db_boletim: BoletimOcorrencia
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :raises SQLAlchemyError: Em caso de qualquer erro no banco de dados, realiza rollback e propaga o erro.
        :return: Não retorna nada (None) em caso de sucesso.
        :rtype: None
        """
        await session.delete(db_boletim)

        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


    async def listar_boletins_completos(self, offset: int, limit: int, session: AsyncSession):
        """
        Lista todos os boletins de ocorrência, carregando ansiosamente os dados do autor e dos declarantes.

        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de dicionários contendo os dados completos dos boletins (incluindo autor e declarantes).
        :rtype: list[dict]
        """
        stmt = (
            select(BoletimOcorrencia)
            .options(
                selectinload(BoletimOcorrencia.autor),
                selectinload(BoletimOcorrencia.declarantes),
            ).offset(offset).limit(limit))
            

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



    async def boletins_com_mais_de_um_declarante(self, offset: int, limit: int, session: AsyncSession):
        """
        Consulta boletins de ocorrência que possuem mais de um declarante, retornando o boletim e a contagem.

        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de dicionários contendo o boletim e o total de declarantes.
        :rtype: list[dict]
        """
        stmt = (
            select(
                BoletimOcorrencia,
                func.count(DeclaranteBoletim.declarante_id).label("total")
            )
            .join(DeclaranteBoletim)
            .group_by(BoletimOcorrencia.id_boletim)
            .having(func.count(DeclaranteBoletim.declarante_id) > 1)
            .offset(offset)
            .limit(limit)
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


    async def boletins_por_posto(self, posto: str, offset: int, limit: int, session: AsyncSession):
        """
        Busca boletins de ocorrência registrados por autores de um posto específico.

        :param posto: O nome ou identificador do posto do autor.
        :type posto: str
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de tuplas contendo o BoletimOcorrencia e o Autor.
        :rtype: list[tuple[BoletimOcorrencia, Autor]]
        """
        stmt = (
        select(BoletimOcorrencia)
        .join(BoletimOcorrencia.autor)
        .where(Autor.posto == posto)
        .offset(offset)
        .limit(limit)
        )
        result = await session.exec(stmt)
        return result.all()

    async def boletins_abertos_por_lotacao_com_multiplos_declarantes(self, lotacao: str, offset: int, limit: int, session: AsyncSession):
        """
        Busca boletins registrados com status 'REGISTRADO' por autores de uma lotação específica e que tenham mais de um declarante.

        :param lotacao: O nome ou identificador da lotação do autor.
        :type lotacao: str
        :param session: Sessão assíncrona do banco de dados.
        :type session: AsyncSession
        :return: Uma lista de tuplas contendo dados sumarizados dos boletins.
        :rtype: list[tuple]
        """
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
            .offset(offset)
            .limit(limit)
        )

        result = await session.exec(stmt)
        rows = result.all()
        return [
            {
                "id_boletim": r[0],
                "data_registro": r[1],
                "tipo_ocorrencia": r[2],
                "descricao": r[3],
                "status": r[4],
                "nome_autor": r[5],
                "lotacao_autor": r[6],
                "total_declarantes": r[7],
            }
            for r in rows
        ]