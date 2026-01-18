from fastapi import APIRouter, status
from schemas.autor import AutorCreate, AutorResponse, AutorRanking
from service.autor import AutorService
from beanie.odm.fields import PydanticObjectId

router = APIRouter(
    prefix="/autores",
    tags=["Autores"],
)

service = AutorService()

@router.post(
    path="/",
    response_model=AutorResponse,
    status_code=status.HTTP_201_CREATED,
    description="cria um autor"
)
async def create_autor(autor: AutorCreate):
    return await service.create_autor(autor)


@router.get(
    path="/",
    response_model=list[AutorResponse],
    status_code=status.HTTP_200_OK,
    description="busca os autores cadastrados"        
)
async def read_autores(skip: int = 0, limit: int = 50):
    return await service.list_autores(skip, limit)


@router.get(
    path="/ranking",
    response_model=list[AutorRanking],
    status_code=status.HTTP_200_OK,
    description="busca os autores que mais registraram boletins"
) 
async def ranking_autores_route(skip: int = 0, limit: int = 50):
    #try:
    return await service.ranking_autores(skip, limit)
    """
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao executar a consulta complexa no banco de dados. Detalhe: {e.args[0]}"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro inesperado no servidor."
        )
        """


@router.get(
    path="/{id_autor}",
    response_model=AutorResponse,
    status_code=status.HTTP_200_OK,
    description="busca um autor por id"        
)
async def read_autor(
    id_autor: PydanticObjectId
):
    return await service.get_autor(id_autor)
    # if not autor:
    #     raise HTTPException(status_code=404, detail="Autor não encontrado")
    

@router.put(
    path="/{id_autor}",
    response_model=AutorResponse,
    status_code=status.HTTP_200_OK,
    description="edita um autor"    
)
async def update_autor(
    id_autor: PydanticObjectId,
    autor: AutorResponse
):
    
    return await service.update_autor(id_autor, autor)
    #     if not result:
    #         raise HTTPException(status_code=404, detail="Autor não encontrado")
    #     return result
    # except IntegrityError as e:
    #     raise HTTPException(status_code=409, detail=str(e))
    # except SQLAlchemyError as e:
    #     raise HTTPException(status_code=500, detail=str(e))


@router.delete(
    path="/{id_autor}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="deleta um autor"
)
async def delete_autor(id_autor: PydanticObjectId):
    await service.delete_autor(id_autor)
    # if not deleted:
    #     raise HTTPException(status_code=404, detail="Autor não encontrado")
    # return {"ok": True, "message": f"Autor com ID {id_autor} deletado com sucesso."}
