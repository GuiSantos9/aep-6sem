from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from pymongo.database import Database

from app.enums.prioridade import PrioridadeEnum
from app.enums.status import StatusDenuncia
from app.enums.tipo import TipoArquiteturaHostil
from app.repositories.denuncia_repository import DenunciaRepository
from app.repositories.vinculo_repository import VinculoRepository
from app.schemas.denuncia import (
    DenunciaCreate,
    DenunciaListResponse,
    DenunciaResponse,
    DenunciaUpdate,
)
from app.schemas.vinculo import VinculoCreate, VinculoResponse, VinculoUpdate
from app.services.denuncia_service import DenunciaService
from app.services.vinculo_service import VinculoService
from db.connection import get_database

router = APIRouter(prefix="/denuncias", tags=["Denúncias"])
MongoDatabase = Annotated[Database, Depends(get_database)]


def get_denuncia_service(database: MongoDatabase) -> DenunciaService:
    return DenunciaService(
        DenunciaRepository(database),
        VinculoRepository(database),
    )


def get_vinculo_service(database: MongoDatabase) -> VinculoService:
    return VinculoService(
        VinculoRepository(database),
        DenunciaRepository(database),
    )


@router.post(
    "",
    response_model=DenunciaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_denuncia(
    payload: DenunciaCreate,
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
):
    return service.create(payload)


@router.get("", response_model=DenunciaListResponse)
def listar_denuncias(
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
    tipo: TipoArquiteturaHostil | None = None,
    prioridade: PrioridadeEnum | None = None,
    status_denuncia: Annotated[
        StatusDenuncia | None,
        Query(alias="status"),
    ] = None,
    cidade: str | None = None,
    bairro: str | None = None,
    orgao_nome: str | None = None,
    busca: Annotated[str | None, Query(min_length=2, max_length=100)] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    items, total = service.list(
        tipo=tipo,
        prioridade=prioridade,
        status=status_denuncia,
        cidade=cidade,
        bairro=bairro,
        orgao_nome=orgao_nome,
        busca=busca,
        limit=limit,
        offset=offset,
    )
    return DenunciaListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{denuncia_id}", response_model=DenunciaResponse)
def buscar_denuncia(
    denuncia_id: str,
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
):
    return service.get(denuncia_id)


@router.patch("/{denuncia_id}", response_model=DenunciaResponse)
def atualizar_denuncia(
    denuncia_id: str,
    payload: DenunciaUpdate,
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
):
    return service.update(denuncia_id, payload)


@router.delete("/{denuncia_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_denuncia(
    denuncia_id: str,
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
) -> Response:
    service.delete(denuncia_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{denuncia_id}/vinculos",
    response_model=VinculoResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_vinculo(
    denuncia_id: str,
    payload: VinculoCreate,
    service: Annotated[VinculoService, Depends(get_vinculo_service)],
):
    return service.create(denuncia_id, payload)


@router.get(
    "/{denuncia_id}/vinculos",
    response_model=list[VinculoResponse],
)
def listar_vinculos(
    denuncia_id: str,
    service: Annotated[VinculoService, Depends(get_vinculo_service)],
):
    return service.list(denuncia_id)


@router.patch(
    "/{denuncia_id}/vinculos/{vinculo_id}",
    response_model=VinculoResponse,
)
def atualizar_vinculo(
    denuncia_id: str,
    vinculo_id: str,
    payload: VinculoUpdate,
    service: Annotated[VinculoService, Depends(get_vinculo_service)],
):
    return service.update(denuncia_id, vinculo_id, payload)


@router.delete(
    "/{denuncia_id}/vinculos/{vinculo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_vinculo(
    denuncia_id: str,
    vinculo_id: str,
    service: Annotated[VinculoService, Depends(get_vinculo_service)],
) -> Response:
    service.delete(denuncia_id, vinculo_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

