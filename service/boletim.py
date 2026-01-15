
from schemas.boletim import BoletimOcorrenciaCreate, BoletimOcorrenciaResponse, BoletimOcorrenciaResponseMultiplosDeclarantes

class BoletimService:

    def __init__(self):
        """
        Inicializa o serviço de Boletim, instanciando o repositório correspondente.
        """
    async def create_boletim(self, boletim: BoletimOcorrenciaCreate) -> BoletimOcorrenciaResponse:
        """
        Cria um novo boletim de ocorrência no banco de dados.

        :param boletim: Dados básicos do boletim a ser criado.
        :type boletim: BoletimOcorrenciaCreate
        :return: O objeto Boletim de Ocorrência criado.
        :rtype: BoletimOcorrencia
        """
        pass

    async def list_boletins(self, offset: int, limit: int) -> list[BoletimOcorrenciaResponse]:
        """
        Lista boletins de ocorrência com paginação.

        :param offset: Posição inicial para a listagem (deslocamento).
        :type offset: int
        :param limit: Número máximo de boletins a serem retornados.
        :type limit: int
        :return: Uma lista de objetos BoletimOcorrencia.
        :rtype: list[BoletimOcorrencia]
        """
        pass

    async def get_boletim(self, id_boletim: int) -> BoletimOcorrenciaResponse:
        """
        Busca um boletim de ocorrência pelo seu ID.

        :param id_boletim: O ID do boletim a ser buscado.
        :type id_boletim: int
        :return: O objeto Boletim de Ocorrência encontrado.
        :rtype: BoletimOcorrencia
        """
        pass
    async def update_boletim(self, id_boletim: int, boletim: BoletimOcorrenciaCreate) -> BoletimOcorrenciaResponse:
        """
        Atualiza os dados de um boletim de ocorrência existente.

        :param id_boletim: O ID do boletim a ser atualizado.
        :type id_boletim: int
        :param boletim: Novos dados básicos do boletim.
        :type boletim: BoletimOcorrenciaCreate
        :return: O objeto Boletim de Ocorrência atualizado.
        :rtype: BoletimOcorrencia
        """
        pass

    async def delete_boletim(self, id_boletim: int) -> BoletimOcorrenciaResponse:
        """
        Deleta um boletim de ocorrência pelo seu ID.

        :param id_boletim: O ID do boletim a ser deletado.
        :type id_boletim: int
        :return: O objeto Boletim que foi deletado.
        :rtype: BoletimOcorrenciaResponse
        """
        pass

    async def boletins_com_mais_de_um_declarante(self, offset: int, limit: int) -> list[BoletimOcorrenciaResponseMultiplosDeclarantes]:
        """
        Lista boletins de ocorrência que possuem mais de um declarante associado.

        :return: Uma lista de boletins com múltiplos declarantes.
        :rtype: list[BoletimOcorrenciaResponse]
        """
        pass

    async def boletins_por_posto(self, posto: str, offset: int, limit: int) -> list[BoletimOcorrenciaResponse]:
        """
        Lista boletins de ocorrência registrados por um posto específico.

        :param posto: O nome ou identificador do posto.
        :type posto: str
        :return: Uma lista de boletins associados ao posto.
        :rtype: list[BoletimOcorrenciaResponse]
        """
        pass
    async def boletins_abertos_por_lotacao_com_multiplos_declarantes(self, lotacao: str, offset: int, limit: int) -> list[BoletimOcorrenciaResponse]:
        """
        Lista boletins de ocorrência que estão abertos, foram registrados em uma lotação específica e possuem múltiplos declarantes.

        :param lotacao: O nome ou identificador da lotação.
        :type lotacao: str
        :return: Uma lista de boletins que atendem aos critérios.
        :rtype: list[BoletimOcorrenciaResponse]
        """

        pass