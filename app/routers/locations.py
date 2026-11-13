from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from pymongo.database import Database

from app.repositories.report_repository import DenunciaRepository
from app.repositories.location_repository import LocalRepository
from app.schemas.report import DenunciaListResponse
from app.schemas.location import LocalCreate, LocalListResponse, LocalResponse
from app.services.report_service import DenunciaService
from app.services.location_service import LocalService
from db.connection import get_database

router = APIRouter(prefix="/locais", tags=["Locais"])
MongoDatabase = Annotated[Database, Depends(get_database)]


def get_local_service(database: MongoDatabase) -> LocalService:
    return LocalService(LocalRepository(database))


def get_denuncia_service(database: MongoDatabase) -> DenunciaService:
    return DenunciaService(DenunciaRepository(database), LocalRepository(database))


LocalServiceDep = Annotated[LocalService, Depends(get_local_service)]


@router.post("", response_model=LocalResponse, status_code=status.HTTP_201_CREATED)
def create_local(payload: LocalCreate, service: LocalServiceDep):
    return service.create(payload)


@router.get("", response_model=LocalListResponse)
def list_locais(service: LocalServiceDep):
    items = service.list()
    return LocalListResponse(items=items, total=len(items))


@router.get("/{local_id}", response_model=LocalResponse)
def get_local(local_id: str, service: LocalServiceDep):
    return service.get(local_id)


@router.get("/{local_id}/denuncias", response_model=DenunciaListResponse)
def list_denuncias_do_local(
    local_id: str,
    locais: LocalServiceDep,
    denuncias: Annotated[DenunciaService, Depends(get_denuncia_service)],
):
    locais.get(local_id)
    items, total = denuncias.list(
        tipo=None, prioridade=None, local_id=local_id, limit=100, offset=0
    )
    return DenunciaListResponse(items=items, total=total, limit=100, offset=0)


@router.delete("/{local_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_local(local_id: str, service: LocalServiceDep) -> Response:
    service.delete(local_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
