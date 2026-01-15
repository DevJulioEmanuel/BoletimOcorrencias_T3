
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
        :rtype: AutorResponse
        """
        pass
    async def list_autores(self, offset: int, limit: int) -> list[AutorResponse]:
        """
        Lista autores com paginação.

        :param offset: Posição inicial para a listagem (deslocamento).
        :type offset: int
        :param limit: Número máximo de autores a serem retornados.
        :type limit: int
        :rtype: list[AutorResponse]
        """
        pass

    async def get_autor(self, id_autor: int) -> AutorResponse | None:
        """
        Busca um autor pelo seu ID.

        :param id_autor: O ID do autor a ser buscado.
        :type id_autor: int
        :return: O objeto Autor encontrado ou None se não existir.
        :rtype: AutorResponse | None
        """
        pass

    async def update_autor(self, id_autor: int, autor: AutorCreate) -> AutorResponse:
        """
        Atualiza os dados de um autor existente.

        :param id_autor: O ID do autor a ser atualizado.
        :type id_autor: int
        :param autor: Novos dados básicos do autor.
        :type autor: AutorCreate
        :return: O objeto Autor atualizado.
        :rtype: AutorResponse
        """
        pass

    async def delete_autor(self, id_autor: int) -> AutorResponse:
        """
        Deleta um autor pelo seu ID.

        :param id_autor: O ID do autor a ser deletado.
        :type id_autor: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :return: O objeto Autor deletado.
        :rtype: AutorResponse
        """
        pass