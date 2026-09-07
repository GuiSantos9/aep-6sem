from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo import DESCENDING
from pymongo.database import Database

from app.entities.denuncia import DenunciaModel
from app.enums.prioridade import PrioridadeEnum
from app.enums.tipo import TipoEnum


def converter_object_id(value: str) -> ObjectId | None:
    try:
        return ObjectId(value)
    except Exception:
        return None


class DenunciaRepository:
    def __init__(self, database: Database) -> None:
        self.collection = database.denuncias

    def create(self, data: dict[str, Any]) -> DenunciaModel:
        agora = datetime.now(timezone.utc)
        document: DenunciaModel = {
            **data,
            "criado_em": agora,
        }
        result = self.collection.insert_one(document)
        return self.collection.find_one({"_id": result.inserted_id})

    def get_by_id(self, denuncia_id: str) -> DenunciaModel | None:
        object_id = converter_object_id(denuncia_id)
        if not object_id:
            return None
        return self.collection.find_one({"_id": object_id})

    def list(
        self,
        *,
        tipo: TipoEnum | None = None,
        prioridade: PrioridadeEnum | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[DenunciaModel], int]:
        query: dict[str, Any] = {}

        if tipo:
            query["tipo"] = tipo.value
        if prioridade:
            query["prioridade"] = prioridade.value

        total = self.collection.count_documents(query)
        cursor = (
            self.collection.find(query)
            .sort("criado_em", DESCENDING)
            .skip(offset)
            .limit(limit)
        )
        return list(cursor), total

    def update(
        self,
        denuncia_id: str,
        data: dict[str, Any],
    ) -> DenunciaModel | None:
        object_id = converter_object_id(denuncia_id)
        if not object_id:
            return None

        data["atualizado_em"] = datetime.now(timezone.utc)
        self.collection.update_one({"_id": object_id}, {"$set": data})
        return self.collection.find_one({"_id": object_id})

    def delete(self, denuncia_id: str) -> bool:
        object_id = converter_object_id(denuncia_id)
        if not object_id:
            return False
        return self.collection.delete_one({"_id": object_id}).deleted_count == 1
