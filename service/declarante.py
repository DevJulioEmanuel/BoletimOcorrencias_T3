
from schemas.declarante import DeclaranteCreate, DeclaranteResponse, DeclaranteNumerosDeRegistros

class DeclaranteService:

    def __init__(self):
        """
        Inicializa o serviço de Declarante, instanciando o repositório correspondente.
        """

    async def create_declarante(self, declarante: DeclaranteCreate) -> DeclaranteResponse:
        """
        Cria um novo declarante no banco de dados.

        :param declarante: Dados básicos do declarante a ser criado.
        :type declarante: DeclaranteCreate
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 409 se houver erro de integridade (ex: CPF já existe).
        :raises HTTPException: Status 500 em caso de outro erro no banco de dados.
        :return: O objeto Declarante criado.
        :rtype: Declarante
        """
        pass

    async def list_declarantes(self, offset: int, limit: int) -> list[DeclaranteResponse]:
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
        pass

    async def get_declarante(self, id_declarante: int) -> DeclaranteResponse:
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
        pass

    async def update_declarante(self, id_declarante: int, data: DeclaranteCreate) -> DeclaranteResponse:
        """
        Atualiza os dados de um declarante existente.

        :param id_declarante: O ID do declarante a ser atualizado.
        :type id_declarante: int
        :param data: Novos dados básicos do declarante.
        :type data: DeclaranteCreate
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises HTTPException: Status 404 se o declarante não for encontrado.
        :raises HTTPException: Status 409 se houver erro de integridade (ex: CPF duplicado).
        :raises HTTPException: Status 500 em caso de outro erro de atualização.
        :return: O objeto Declarante atualizado.
        :rtype: Declarante
        """
        pass

    async def delete_declarante(self, id_declarante: int) -> DeclaranteResponse:
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
        pass

    async def declarantes_reincidentes_por_tipo(self, offset: int, limit: int) -> list[DeclaranteNumerosDeRegistros]:
        """
        Lista declarantes que são considerados 'reincidentes' e agrupa por tipo de ocorrência.

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de declarantes reincidentes agrupados.
        :rtype: list
        """
        pass

    async def declarantes_sem_boletim(self, offset: int, limit: int) -> list[DeclaranteResponse]:
        """
        Lista declarantes que não possuem nenhum boletim de ocorrência associado.

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de declarantes sem boletins.
        :rtype: list[Declarante]
        """
        pass

    async def ranking_declarantes(self, offset: int, limit: int) -> list[DeclaranteNumerosDeRegistros]:
        """
        Gera o ranking de declarantes baseado em algum critério definido (ex: número de participações em boletins).

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: O ranking de declarantes.
        :rtype: list
        """
        pass