from sqlmodel.ext.asyncio.session import AsyncSession
from repository.boletim import BoletimRepository
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from schemas.boletim import BoletimOcorrenciaBase
from sqlmodel.ext.asyncio.session import AsyncSession

from repository.boletim import BoletimRepository


class BoletimService:

    def __init__(self):
        """
        Inicializa o serviço de Boletim, instanciando o repositório correspondente.
        """
        self.repo = BoletimRepository()

    async def create_boletim(self, boletim: BoletimOcorrenciaBase, session: AsyncSession):
        """
        Cria um novo boletim de ocorrência no banco de dados.

        :param boletim: Dados básicos do boletim a ser criado.
        :type boletim: BoletimOcorrenciaBase
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 500 se ocorrer um erro no banco de dados.
        :return: O objeto Boletim de Ocorrência criado.
        :rtype: BoletimOcorrencia
        """
        try:
            return await self.repo.create(boletim, session)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar boletim: {e}"
            )

    async def list_boletins(self, offset: int, limit: int,session: AsyncSession):
        """
        Lista boletins de ocorrência com paginação.

        :param offset: Posição inicial para a listagem (deslocamento).
        :type offset: int
        :param limit: Número máximo de boletins a serem retornados.
        :type limit: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de objetos BoletimOcorrencia.
        :rtype: list[BoletimOcorrencia]
        """
        return await self.repo.list_all(offset, limit, session)

    async def get_boletim(self, id_boletim: int, session: AsyncSession):
        """
        Busca um boletim de ocorrência pelo seu ID.

        :param id_boletim: O ID do boletim a ser buscado.
        :type id_boletim: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 404 se o boletim não for encontrado.
        :return: O objeto Boletim de Ocorrência encontrado.
        :rtype: BoletimOcorrencia
        """
        boletim = await self.repo.get_by_id(id_boletim, session)

        if not boletim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boletim não encontrado"
            )

        return boletim

    async def update_boletim(self, id_boletim: int, boletim: BoletimOcorrenciaBase, session: AsyncSession):
        """
        Atualiza os dados de um boletim de ocorrência existente.

        :param id_boletim: O ID do boletim a ser atualizado.
        :type id_boletim: int
        :param boletim: Novos dados básicos do boletim.
        :type boletim: BoletimOcorrenciaBase
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 404 se o boletim não for encontrado.
        :raises HTTPException: Status 500 se ocorrer um erro no banco de dados durante a atualização.
        :return: O objeto Boletim de Ocorrência atualizado.
        :rtype: BoletimOcorrencia
        """
        db_boletim = await self.repo.get_by_id(id_boletim, session)

        if not db_boletim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boletim não encontrado"
            )

        try:
            return await self.repo.update(db_boletim, boletim, session)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar boletim: {e}"
            )

    async def delete_boletim(self, id_boletim: int, session: AsyncSession):
        """
        Deleta um boletim de ocorrência pelo seu ID.

        :param id_boletim: O ID do boletim a ser deletado.
        :type id_boletim: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 404 se o boletim não for encontrado.
        :raises HTTPException: Status 500 se ocorrer um erro no banco de dados durante a deleção.
        :return: Uma mensagem de confirmação da deleção.
        :rtype: dict
        """
        db_boletim = await self.repo.get_by_id(id_boletim, session)

        if not db_boletim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boletim não encontrado"
            )

        try:
            await self.repo.delete(db_boletim, session)
            return {"ok": True, "message": f"Boletim ID {id_boletim} deletado com sucesso."}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao deletar boletim: {e}"
            )


    async def listar_completos(self, offset: int, limit: int, session: AsyncSession):
        """
        Lista todos os boletins de ocorrência que estão 'completos' (critério definido no repositório).

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de boletins de ocorrência considerados completos.
        :rtype: list[BoletimOcorrencia]
        """
        return await self.repo.listar_boletins_completos(offset, limit, session)

    async def boletins_com_mais_de_um_declarante(self, offset: int, limit: int, session: AsyncSession):
        """
        Lista boletins de ocorrência que possuem mais de um declarante associado.

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de boletins com múltiplos declarantes.
        :rtype: list[BoletimOcorrencia]
        """
        return await self.repo.boletins_com_mais_de_um_declarante(offset, limit, session)

    async def boletins_por_posto(self, posto: str, offset: int, limit: int, session: AsyncSession):
        """
        Lista boletins de ocorrência registrados por um posto específico.

        :param posto: O nome ou identificador do posto.
        :type posto: str
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de boletins associados ao posto.
        :rtype: list[BoletimOcorrencia]
        """
        return await self.repo.boletins_por_posto(posto, offset, limit, session)

    async def boletins_abertos_por_lotacao_com_multiplos_declarantes(self, lotacao: str, offset: int, limit: int, session: AsyncSession):
        """
        Lista boletins de ocorrência que estão abertos, foram registrados em uma lotação específica e possuem múltiplos declarantes.

        :param lotacao: O nome ou identificador da lotação.
        :type lotacao: str
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de boletins que atendem aos critérios.
        :rtype: list[BoletimOcorrencia]
        """
        return await self.repo.boletins_abertos_por_lotacao_com_multiplos_declarantes(lotacao, offset, limit, session)