from sqlmodel.ext.asyncio.session import AsyncSession
from repository.autor import AutorRepository
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas.autor import AutorBase, AutorRanking


class AutorService:

    def __init__(self):
        """
        Inicializa o serviço de Autor, instanciando o repositório correspondente.
        """
        self.repo = AutorRepository()

    async def create_autor(self, autor: AutorBase, session: AsyncSession):
        """
        Cria um novo autor no banco de dados.

        :param autor: Dados básicos do autor a ser criado.
        :type autor: AutorBase
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises IntegrityError: Se a matrícula ou ID do autor já existirem.
        :raises SQLAlchemyError: Em caso de qualquer outro erro no banco de dados.
        :return: O objeto Autor criado.
        :rtype: Autor
        """
        try:
            return await self.repo.create(autor, session)
        except IntegrityError:
            raise IntegrityError("Matrícula ou ID do Autor já existem.", None, None)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Erro no banco de dados: {e}", None, None)

    async def list_autores(self, offset: int, limit: int, session: AsyncSession):
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
        return await self.repo.list(offset, limit, session)

    async def get_autor(self, id_autor: int, session: AsyncSession):
        """
        Busca um autor pelo seu ID.

        :param id_autor: O ID do autor a ser buscado.
        :type id_autor: int
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: O objeto Autor encontrado ou None se não existir.
        :rtype: Autor | None
        """
        return await self.repo.get_by_id(id_autor, session)

    async def update_autor(self, id_autor: int, autor: AutorBase, session: AsyncSession):
        """
        Atualiza os dados de um autor existente.

        :param id_autor: O ID do autor a ser atualizado.
        :type id_autor: int
        :param autor: Novos dados básicos do autor.
        :type autor: AutorBase
        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :raises IntegrityError: Se a atualização violar uma restrição de integridade (ex: duplicidade de matrícula).
        :raises SQLAlchemyError: Em caso de qualquer outro erro de atualização.
        :return: O objeto Autor atualizado.
        :rtype: Autor
        """
        try:
            return await self.repo.update(id_autor, autor, session)
        except IntegrityError:
            raise IntegrityError("Dados violam restrição (ex: matrícula duplicada).", None, None)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"Erro ao atualizar: {e}", None, None)

    async def delete_autor(self, id_autor: int, session: AsyncSession):
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
        try:
            return await self.repo.delete(id_autor, session)
        except IntegrityError as e:
            raise IntegrityError(f"Erro: {e}", None, None)

    async def ranking_autores(self, session: AsyncSession) -> AutorRanking:
        """
        Gera o ranking de autores baseado em algum critério definido (ex: número de boletins).

        :param session: Sessão assíncrona do banco de dados para a operação.
        :type session: AsyncSession
        :return: O ranking de autores.
        :rtype: AutorRanking
        """
        return await self.repo.ranking_autores(session)
