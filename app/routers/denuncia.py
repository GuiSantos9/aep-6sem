from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from pymongo.database import Database

from app.enums.prioridade import PrioridadeEnum
from app.enums.tipo import TipoEnum
from app.repositories.denuncia_repository import DenunciaRepository
from app.schemas.denuncia import (
    DenunciaCreate,
    DenunciaListResponse,
    DenunciaResponse,
    DenunciaUpdate,
)
from app.services.denuncia_service import DenunciaService
from db.connection import get_database

router = APIRouter(prefix="/denuncias", tags=["Denúncias"])
MongoDatabase = Annotated[Database, Depends(get_database)]


def get_denuncia_service(database: MongoDatabase) -> DenunciaService:
    return DenunciaService(DenunciaRepository(database))


@router.post("", response_model=DenunciaResponse, status_code=status.HTTP_201_CREATED)
def create_denuncia(
    payload: DenunciaCreate,
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
):
    return service.create(payload)


@router.get("", response_model=DenunciaListResponse)
def list_denuncias(
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
    tipo: TipoEnum | None = None,
    prioridade: PrioridadeEnum | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    items, total = service.list(
        tipo=tipo,
        prioridade=prioridade,
        limit=limit,
        offset=offset,
    )
    return DenunciaListResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/{denuncia_id}", response_model=DenunciaResponse)
def get_denuncia(
    denuncia_id: str,
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
):
    return service.get(denuncia_id)


@router.patch("/{denuncia_id}", response_model=DenunciaResponse)
def update_denuncia(
    denuncia_id: str,
    payload: DenunciaUpdate,
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
):
    return service.update(denuncia_id, payload)


@router.delete("/{denuncia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_denuncia(
    denuncia_id: str,
    service: Annotated[DenunciaService, Depends(get_denuncia_service)],
) -> Response:
    service.delete(denuncia_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
