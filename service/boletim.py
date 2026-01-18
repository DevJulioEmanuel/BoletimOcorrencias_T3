from fastapi import HTTPException, status

from schemas.boletim import BoletimOcorrenciaCreate, BoletimOcorrenciaResponse, BoletimOcorrenciaResponseMultiplosDeclarantes
from models import BoletimOcorrencia, Autor, Declarante
from beanie import PydanticObjectId
from datetime import date

class BoletimService:

    def __init__(self):
        """
        Inicializa o serviço de Boletim, instanciando o repositório correspondente.
        """
        pass
    async def create_boletim(self, boletim: BoletimOcorrenciaCreate) -> BoletimOcorrencia:
        """
        Cria um novo boletim de ocorrência no banco de dados após validar a existência do autor e dos declarantes informados.

        :param boletim: Esquema com os dados para criação do boletim.
        :return: O documento do Boletim de Ocorrência criado.
        """
        dados = boletim.model_dump()

        autor = await Autor.get(dados.get("autor"))
        if not autor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Autor não encontrado. O boletim precisa de um autor válido."
            )

        ids_declarantes = dados.get("declarantes", [])
        declarantes_encontrados = await Declarante.find(
            {"_id": {"$in": ids_declarantes}}
        ).to_list()

        if len(declarantes_encontrados) != len(ids_declarantes):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um ou mais declarantes informados são inválidos ou não existem."
            )

        try:
            dados["autor"] = autor
            dados["declarantes"] = declarantes_encontrados

            novo_boletim = BoletimOcorrencia(**dados)
            await novo_boletim.insert()
            return novo_boletim

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao persistir o boletim: {str(e)}"
            )

    async def list_boletins(self, skip: int, limit: int) -> list[BoletimOcorrencia]:
        """
        Retorna uma lista de todos os boletins de ocorrência com suporte a paginação e carregamento de vínculos.

        :param skip: Quantidade de registros a serem pulados.
        :param limit: Limite máximo de registros a serem retornados.
        :return: Lista de objetos BoletimOcorrencia.
        """
        return await BoletimOcorrencia.find_all(fetch_links=True).skip(skip).limit(limit).to_list()

    async def get_boletim(self, id_boletim: PydanticObjectId) -> BoletimOcorrencia:
        """
        Recupera um boletim de ocorrência específico pelo ID, incluindo todos os seus vínculos.

        :param id_boletim: Identificador único do boletim.
        :return: O objeto BoletimOcorrencia encontrado.
        """
        boletim = await BoletimOcorrencia.get(id_boletim, fetch_links=True)

        if not boletim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boletim de ocorrência não encontrado"
            )

        return boletim

    async def update_boletim(self, id_boletim: PydanticObjectId, boletim: BoletimOcorrenciaCreate) -> BoletimOcorrencia:
        """
        Atualiza as informações de um boletim existente, validando se o novo autor ou declarantes são válidos no sistema.

        :param id_boletim: Identificador do boletim a ser atualizado.
        :param boletim: Dados atualizados do boletim.
        :return: O documento do Boletim de Ocorrência atualizado.
        """
        boletim_att = await BoletimOcorrencia.get(id_boletim)

        if not boletim_att:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boletim de ocorrência não encontrado para atualização"
            )

        update = boletim.model_dump()

        for key, value in update.items():
            if key in ["autor", "declarantes"]:
                continue
            setattr(boletim_att, key, value)

        if "autor" in update:
            autor = await Autor.get(update["autor"])
            if not autor:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Autor referenciado não encontrado"
                )
            boletim_att.autor = autor

        if "declarantes" in update:
            update_ids = update["declarantes"]
            declarantes_encontrados = await Declarante.find({"_id": {"$in": update_ids}}).to_list()

            if len(declarantes_encontrados) != len(update_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Um ou mais declarantes referenciados são inválidos ou não existem"
                )

            boletim_att.declarantes = declarantes_encontrados

        try:
            await boletim_att.save()
            return boletim_att
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao salvar as alterações do boletim: {str(e)}"
            )

    async def delete_boletim(self, id_boletim: PydanticObjectId) -> BoletimOcorrenciaResponse:
        """
        Exclui permanentemente um boletim de ocorrência da base de dados.

        :param id_boletim: Identificador do boletim a ser removido.
        :return: O documento do boletim que foi excluído.
        """
        boletim = await BoletimOcorrencia.get(id_boletim)

        if not boletim:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Boletim de ocorrência não encontrado para exclusão"
            )

        await boletim.delete()
        return boletim

    async def boletins_com_mais_de_um_declarante(self, skip: int, limit: int) -> list[BoletimOcorrenciaResponseMultiplosDeclarantes]:
        """
        Executa uma agregação para filtrar boletins que possuam dois ou mais declarantes associados.

        :param skip: Quantidade de registros para pular.
        :param limit: Limite de registros para retornar.
        :return: Lista de boletins com a contagem de declarantes.
        """

        pipeline = [
            {"$addFields": {"total_declarantes": {"$size": "$declarantes"}}},
            {"$match": {"total_declarantes": {"$gt": 1}}},
            {"$skip": skip},
            {"$limit": limit},
            {
                "$project": {
                    "id": "$_id",
                    "data_registro": 1,
                    "tipo_ocorrencia": 1,
                    "status": 1,
                    "total_declarantes": 1,
                    "autor": 1,
                    "declarantes": 1,
                    "_id": 0
                }
            }
        ]
        return await BoletimOcorrencia.aggregate(pipeline).to_list()

    async def boletins_por_posto(self, posto: str, skip: int, limit: int) -> list[BoletimOcorrencia]:
        """
        Realiza uma busca pelo posto do autor associado ao boletim.

        :param posto: Termo de busca para o campo posto do autor.
        :param skip: Offset para paginação.
        :param limit: Limite de resultados.
        :return: Lista de boletins filtrados pelo posto.
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "autor",
                    "localField": "autor.$id",
                    "foreignField": "_id",
                    "as": "autor"
                }
            },
            {"$unwind": "$autor"},
            {
                "$match":
                    {
                        "autor.posto":
                            {
                                "$regex": posto,
                                "$options": "i"
                            }
                    }
            },
            {"$skip": skip},
            {"$limit": limit},
            {
                "$project": {
                    "id": "$_id",
                    "data_registro": 1,
                    "tipo_ocorrencia": 1,
                    "descricao": 1,
                    "status": 1,
                    "autor": 1,
                    "_id": 0
                }
            }
        ]
        return await BoletimOcorrencia.aggregate(pipeline).to_list()

    async def boletins_abertos_por_lotacao_com_multiplos_declarantes(self, lotacao: str, skip: int, limit: int) -> list[BoletimOcorrencia]:
        """
        Filtra boletins com status 'Registrado' que pertencem a uma lotação específica e possuem múltiplos declarantes.

        :param lotacao: Termo para busca parcial na lotação do autor.
        :param skip: Parâmetro de deslocamento da busca.
        :param limit: Máximo de itens por página.
        :return: Lista de boletins que atendem aos critérios especificados.
        """
        pipeline = [
            {"$match": {"status": "Registrado"}},
            {
                "$lookup": {
                    "from": "autor",
                    "localField": "autor.$id",
                    "foreignField": "_id",
                    "as": "autor"
                }
            },
            {"$unwind": "$autor"},
            {"$match":
                 {
                     "autor.lotacao":
                         {
                             "$regex": lotacao,
                             "$options": "i"
                         }
                 }
            },
            {
                "$addFields":
                    {
                        "total_declarantes":
                         {
                             "$size": "$declarantes"
                         }
                    }
            },
            {"$match": {"total_declarantes": {"$gt": 1}}},
            {"$skip": skip},
            {"$limit": limit},
            {
                "$project": {
                    "id": "$_id",
                    "data_registro": 1,
                    "tipo_ocorrencia": 1,
                    "descricao": 1,
                    "status": 1,
                    "autor": 1,
                    "declarantes": 1,
                    "_id": 0
                }
            }
        ]
        return await BoletimOcorrencia.aggregate(pipeline).to_list()

    async def boletins_por_data(self, data: date, skip: int, limit: int) -> list[BoletimOcorrencia]:
        """
        Lista todos os boletins de ocorrência registrados em uma data específica.

        :param data: Objeto de data para o filtro.
        :param skip: Quantidade de itens a serem ignorados no início da lista.
        :param limit: Quantidade máxima de itens a serem retornados.
        :return: Lista de boletins correspondentes à data informada.
        """
        try:
            return await BoletimOcorrencia.find({"data_registro":data} ,fetch_links=True).skip(skip).limit(limit).to_list()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao filtrar boletins por data: {str(e)}"
            )