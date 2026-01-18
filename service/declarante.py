from unittest import skip

from fastapi import HTTPException, status
from schemas.declarante import DeclaranteCreate, DeclaranteResponse, DeclaranteNumerosDeRegistros
from beanie import PydanticObjectId
from models import Declarante, BoletimOcorrencia


class DeclaranteService:

    def __init__(self):
        pass

    async def create_declarante(self, declarante: DeclaranteCreate) -> DeclaranteResponse:
        """
        Cria um novo registro de declarante na base de dados.

        :param declarante: Esquema contendo os dados para criação.
        :return: Objeto do declarante persistido.
        """
        try:
            novo_declarante = Declarante(**declarante.model_dump())
            await novo_declarante.insert()
            return novo_declarante
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar declarante: {str(e)}"
            )

    async def list_declarantes(self, skip: int, limit: int) -> list[DeclaranteResponse]:
        """
        Recupera uma lista de declarantes com suporte a paginação.

        :param skip: Número de registros a ignorar.
        :param limit: Número máximo de registros a retornar.
        :return: Lista de declarantes encontrados.
        """
        try:
            return await Declarante.find_all().skip(skip).limit(limit).to_list()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao listar declarantes: {str(e)}"
            )

    async def get_declarante(self, id_declarante: PydanticObjectId) -> DeclaranteResponse:
        """
        Busca um declarante específico pelo seu identificador único.

        :param id_declarante: ID do declarante no formato PydanticObjectId.
        :return: Dados do declarante encontrado.
        """
        declarante = await Declarante.get(id_declarante)

        if not declarante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Declarante não encontrado"
            )

        return declarante

    async def update_declarante(self, id_declarante: PydanticObjectId, data: DeclaranteCreate) -> DeclaranteResponse:
        """
        Atualiza as informações de um declarante existente.

        :param id_declarante: ID do declarante a ser atualizado.
        :param data: Novos dados para atualização.
        :return: Objeto do declarante atualizado.
        """
        declarante_att = await Declarante.get(id_declarante)

        if not declarante_att:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Declarante não encontrado para atualização"
            )

        try:
            update = data.model_dump()
            for key, value in update.items():
                setattr(declarante_att, key, value)

            await declarante_att.save()
            return declarante_att
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao atualizar declarante: {str(e)}"
            )
    async def delete_declarante(self, id_declarante: PydanticObjectId):
        """
        Remove um declarante do sistema.

        :param id_declarante: ID do declarante a ser excluído.
        :return: Dicionário confirmando a exclusão.
        """

        declarante = await Declarante.get(id_declarante)

        if not declarante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Declarante não encontrado para exclusão"
            )

        await declarante.delete()
        return {"detail": "Declarante deletado com sucesso"}

    async def declarantes_reincidentes_por_tipo(self, skip: int, limit: int) -> list[DeclaranteNumerosDeRegistros]:
        """
        Identifica declarantes vinculados a múltiplos boletins de um mesmo tipo.

        Utiliza pipeline de agregação para agrupar por ID e tipo de ocorrência, filtrando contagens superiores a um.

        :param skip: Offset para paginação.
        :param limit: Limite de registros.
        :return: Lista de reincidentes com total de registros.
        """
        try:
            pipeline = [
                {"$unwind": "$declarantes"},
                {
                    "$group": {
                        "_id": {
                            "id": "$declarantes.$id",
                            "tipo_ocorrencia": "$tipo_ocorrencia"
                        },
                        "total": {"$sum": 1}
                    }
                },
                {"$match": {"total": {"$gt": 1}}},
                {
                    "$lookup": {
                        "from": "declarantes",
                        "localField": "_id.id",
                        "foreignField": "_id",
                        "as": "perfil"
                    }
                },
                {"$unwind": "$perfil"},
                {"$sort": {"total": -1}},
                {"$skip": skip},
                {"$limit": limit},
                {
                    "$project": {
                        "id": "$_id.id",
                        "nome": "$perfil.nome",
                        "cpf": "$perfil.cpf",
                        "endereco": "$perfil.endereco",
                        "tipo_envolvimento": "$perfil.tipo_envolvimento",
                        "quantidade_registros": "$total",
                        "_id": 0
                    }
                }
            ]

            return await BoletimOcorrencia.aggregate(pipeline).to_list()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao processar reincidência: {str(e)}"
            )

    async def declarantes_sem_boletim(self, skip: int, limit: int) -> list[DeclaranteNumerosDeRegistros]:
        """
        Localiza declarantes que não possuem nenhum vínculo com boletins de ocorrência.

        Realiza um lookup na coleção de boletins e filtra documentos com lista de correspondência vazia.

        :param skip: Offset para paginação.
        :param limit: Limite de registros.
        :return: Lista de declarantes sem boletins.
        """

        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": "boletins",
                        "localField": "_id",
                        "foreignField": "declarantes.$id",
                        "as": "boletins_encontrados"
                    }
                },
                {
                    "$match": {
                        "boletins_encontrados": {"$size": 0}
                    }
                },
                {
                    "$addFields": {
                        "quantidade_registros": 0
                    }
                },
                {"$skip": skip},
                {"$limit": limit},
                {
                    "$project": {
                        "id": "$_id",
                        "nome": 1,
                        "cpf": 1,
                        "endereco": 1,
                        "tipo_envolvimento": 1,
                        "quantidade_registros": 1,
                        "_id": 0
                    }
                }
            ]

            return await Declarante.aggregate(pipeline).to_list()

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro: {str(e)}"
            )

    async def ranking_declarantes(self, skip: int, limit: int) -> list[DeclaranteNumerosDeRegistros]:
        """
        Gera um ranking geral de declarantes baseado no volume de participações em boletins.

        Agrupa as ocorrências por declarante e ordena de forma decrescente pela quantidade.

        :param skip: Offset para paginação.
        :param limit: Limite de registros.
        :return: Lista ordenada de declarantes e seu total de registros.
        """
        try:
            pipeline = [
                {"$unwind": "$declarantes"},
                {
                    "$group": {
                        "_id": "$declarantes.$id",
                        "quantidade_registros": {"$sum": 1}
                    }
                },
                {
                    "$lookup": {
                        "from": "declarantes",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "dados_declarantes"
                    }
                },
                {"$unwind": "$dados_declarantes"},
                {"$sort": {"quantidade_registros": -1}},
                {"$skip": skip},
                {"$limit": limit},
                {
                    "$project": {
                        "id": "$_id",
                        "nome": "$dados_declarantes.nome",
                        "cpf": "$dados_declarantes.cpf",
                        "endereco": "$dados_declarantes.endereco",
                        "tipo_envolvimento": "$dados_declarantes.tipo_envolvimento",
                        "quantidade_registros": 1,
                        "_id": 0
                    }
                }
            ]

            resultados = await BoletimOcorrencia.aggregate(pipeline).to_list()
            return resultados

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao processar ranking de declarantes: {str(e)}"
            )