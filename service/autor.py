
from schemas.autor import AutorCreate, AutorResponse


class AutorService:

    def __init__(self):
        """
        Inicializa o serviço de Autor, instanciando o repositório correspondente.
        """

    async def create_autor(self, autor: AutorCreate) -> AutorResponse:
        """
        Cria um novo autor no banco de dados.

        :param autor: Dados básicos do autor a ser criado.
        :type autor: AutorCreate
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises IntegrityError: Se a matrícula ou ID do autor já existirem.
        :raises SQLAlchemyError: Em caso de qualquer outro erro no banco de dados.
        :return: O objeto Autor criado.
        :rtype: Autor
        """
        pass
    async def list_autores(self, offset: int, limit: int) -> list[AutorResponse]:
        """
        Lista autores com paginação.

        :param offset: Posição inicial para a listagem (deslocamento).
        :type offset: int
        :param limit: Número máximo de autores a serem retornados.
        :type limit: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: Uma lista de objetos Autor.
        :rtype: list[Autor]
        """
        pass

    async def get_autor(self, id_autor: int) -> AutorResponse:
        """
        Busca um autor pelo seu ID.

        :param id_autor: O ID do autor a ser buscado.
        :type id_autor: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: O objeto Autor encontrado ou None se não existir.
        :rtype: Autor | None
        """
        pass

    async def update_autor(self, id_autor: int, autor: AutorCreate) -> AutorResponse:
        """
        Atualiza os dados de um autor existente.

        :param id_autor: O ID do autor a ser atualizado.
        :type id_autor: int
        :param autor: Novos dados básicos do autor.
        :type autor: AutorCreate
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises IntegrityError: Se a atualização violar uma restrição de integridade (ex: duplicidade de matrícula).
        :raises SQLAlchemyError: Em caso de qualquer outro erro de atualização.
        :return: O objeto Autor atualizado.
        :rtype: Autor
        """
        pass

    async def delete_autor(self, id_autor: int) -> AutorResponse:
        """
        Deleta um autor pelo seu ID.

        :param id_autor: O ID do autor a ser deletado.
        :type id_autor: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises IntegrityError: Se houver erro de integridade ao tentar deletar (ex: chave estrangeira).
        :return: O objeto Autor deletado.
        :rtype: Autor
        """
        pass
    """ 
    async def ranking_autores(self, offset: int, limit: int, session: AsyncSession) -> AutorRanking:
        Gera o ranking de autores baseado em algum critério definido (ex: número de boletins).

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: O ranking de autores.
        :rtype: AutorRanking
        return await self.repo.ranking_autores(offset, limit, session)
    """