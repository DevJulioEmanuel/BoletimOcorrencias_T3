from sqlmodel.ext.asyncio.session import AsyncSession
from repository.declarante import DeclaranteRepository
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from repository.declarante import DeclaranteRepository
from schemas.declarante import DeclaranteBase

class DeclaranteService:

    def __init__(self):
        """
        Inicializa o serviço de Declarante, instanciando o repositório correspondente.
        """
        self.repo = DeclaranteRepository()

    async def create_declarante(self, declarante: DeclaranteBase, session: AsyncSession):
        """
        Cria um novo declarante no banco de dados.

        :param declarante: Dados básicos do declarante a ser criado.
        :type declarante: DeclaranteBase
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 409 se houver erro de integridade (ex: CPF já existe).
        :raises HTTPException: Status 500 em caso de outro erro no banco de dados.
        :return: O objeto Declarante criado.
        :rtype: Declarante
        """
        try:
            return await self.repo.create(declarante, session)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade: CPF já existe ou outra restrição foi violada."
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro no banco de dados: {e}"
            )

    async def list_declarantes(self, offset: int, limit: int, session: AsyncSession):
        """
        Lista declarantes com paginação.

        :param offset: Posição inicial para a listagem (deslocamento).
        :type offset: int
        :param limit: Número máximo de declarantes a serem retornados.
        :type limit: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de objetos Declarante.
        :rtype: list[Declarante]
        """
        return await self.repo.list_all(offset, limit, session)

    async def get_declarante(self, id_declarante: int, session: AsyncSession):
        """
        Busca um declarante pelo seu ID.

        :param id_declarante: O ID do declarante a ser buscado.
        :type id_declarante: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 404 se o declarante não for encontrado.
        :return: O objeto Declarante encontrado.
        :rtype: Declarante
        """
        declarante = await self.repo.get_by_id(id_declarante, session)

        if not declarante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Declarante não encontrado"
            )

        return declarante

    async def update_declarante(self, id_declarante: int, data: DeclaranteBase, session: AsyncSession):
        """
        Atualiza os dados de um declarante existente.

        :param id_declarante: O ID do declarante a ser atualizado.
        :type id_declarante: int
        :param data: Novos dados básicos do declarante.
        :type data: DeclaranteBase
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 404 se o declarante não for encontrado.
        :raises HTTPException: Status 409 se houver erro de integridade (ex: CPF duplicado).
        :raises HTTPException: Status 500 em caso de outro erro de atualização.
        :return: O objeto Declarante atualizado.
        :rtype: Declarante
        """
        db_declarante = await self.repo.get_by_id(id_declarante, session)

        if not db_declarante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Declarante não encontrado"
            )

        try:
            return await self.repo.update(db_declarante, data, session)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Erro de integridade (ex: CPF duplicado)."
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar no banco: {e}"
            )

    async def delete_declarante(self, id_declarante: int, session: AsyncSession):
        """
        Deleta um declarante pelo seu ID.

        :param id_declarante: O ID do declarante a ser deletado.
        :type id_declarante: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 404 se o declarante não for encontrado.
        :raises HTTPException: Status 500 se ocorrer um erro no banco de dados durante a deleção.
        :return: Uma mensagem de confirmação da deleção.
        :rtype: dict
        """
        db_declarante = await self.repo.get_by_id(id_declarante, session)

        if not db_declarante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Declarante não encontrado"
            )

        try:
            await self.repo.delete(db_declarante, session)
            return {"ok": True, "message": f"Declarante com ID {id_declarante} deletado com sucesso."}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao deletar: {e}"
            )

    async def declarantes_reincidentes_por_tipo(self, session: AsyncSession):
        """
        Lista declarantes que são considerados 'reincidentes' e agrupa por tipo de ocorrência.

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de declarantes reincidentes agrupados.
        :rtype: list
        """
        return await self.repo.declarantes_reincidentes_por_tipo(session)

    async def declarantes_sem_boletim(self, session: AsyncSession):
        """
        Lista declarantes que não possuem nenhum boletim de ocorrência associado.

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de declarantes sem boletins.
        :rtype: list[Declarante]
        """
        return await self.repo.declarantes_sem_boletim(session)

    async def ranking_declarantes(self, session: AsyncSession):
        """
        Gera o ranking de declarantes baseado em algum critério definido (ex: número de participações em boletins).

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: O ranking de declarantes.
        :rtype: list
        """
        return await self.repo.ranking_declarantes(session)