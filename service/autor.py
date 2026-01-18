from fastapi import HTTPException, status
from schemas.autor import AutorCreate, AutorResponse, AutorRanking
from beanie import PydanticObjectId
from models import Autor, BoletimOcorrencia


class AutorService:

    def __init__(self):
        pass

    async def create_autor(self, autor: AutorCreate) -> AutorResponse:
        """
        Cria um novo autor no banco.

        :param autor: Esquema contendo os dados básicos para criação (nome, matrícula, posto, lotação).
        :return: O documento do Autor criado com seu ID gerado.
        """
        try:
            novo_autor = Autor(**autor.model_dump())
            await novo_autor.insert()
            return novo_autor
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar autor: {str(e)}"
            )

    async def list_autores(self, skip: int, limit: int) -> list[AutorResponse]:
        """
        Recupera uma lista paginada de todos os autores cadastrados.

        :param skip: Quantidade de registros a serem ignorados no início.
        :param limit: Quantidade máxima de registros a serem retornados.
        :return: Lista de objetos AutorResponse.
        """
        return await Autor.find_all().skip(skip).limit(limit).to_list()

    async def ranking_autores(self, skip: int, limit: int) -> list[AutorRanking]:
        """
        Executa uma agregação para ranquear os autores de acordo com o número de boletins registrados.

        O pipeline agrupa os boletins pelo ID do autor, realiza um lookup para buscar os dados cadastrais
        e ordena os resultados de forma decrescente.

        :param skip: Offset para a paginação dos resultados.
        :param limit: Limite de autores a serem exibidos no ranking.
        :return: Lista de autores e seus respectivos totais de boletins.
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$autor.$id",
                    "total_boletins": {"$sum": 1}
                }
            },
            {
                "$lookup": {
                    "from": "autor",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "dados_autor"
                }
            },
            {"$unwind": "$dados_autor"},
            {"$sort": {"total_boletins": -1}},
            {"$skip": skip},
            {"$limit": limit},
            {
                "$project": {
                    "id": "$_id",
                    "nome": "$dados_autor.nome",
                    "matricula": "$dados_autor.matricula",
                    "posto": "$dados_autor.posto",
                    "lotacao": "$dados_autor.lotacao",
                    "total_boletins": 1,
                    "_id": 0
                }
            }
        ]
        return await BoletimOcorrencia.aggregate(pipeline).to_list()

    async def get_autor(self, id_autor: PydanticObjectId) -> AutorResponse:
        """
        Recupera os dados de um autor específico.

        :param id_autor: Identificador único do autor (ObjectId).
        :return: O documento do Autor encontrado.
        """
        autor = await Autor.get(id_autor)

        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Autor não encontrado"
            )

        return autor

    async def update_autor(self, id_autor: PydanticObjectId, autor: AutorResponse) -> AutorResponse:
        """
        Atualiza todos os campos de um autor existente de forma dinâmica.

        :param id_autor: Identificador do autor a ser modificado.
        :param autor: Esquema contendo os novos dados para atualização.
        :return: O documento do Autor após a persistência das alterações.
        """
        autor_att = await Autor.get(id_autor)

        if not autor_att:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Autor não encontrado para atualização"
            )

        update = autor.model_dump()
        for key, value in update.items():
            setattr(autor_att, key, value)

        await autor_att.save()
        return autor_att

    async def delete_autor(self, id_autor: PydanticObjectId):
        """
        Remove um autor da base de dados e retorna uma confirmação de sucesso.

        :param id_autor: Identificador do autor a ser removido.
        :return: Dicionário contendo a mensagem de sucesso.
        """
        autor = await Autor.get(id_autor)

        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Autor não encontrado para exclusão"
            )

        await autor.delete()
        return {"detail": "Autor deletado com sucesso"}