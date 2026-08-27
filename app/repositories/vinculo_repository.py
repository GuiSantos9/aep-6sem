from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo import DESCENDING
from pymongo.database import Database

from app.entities.vinculo import VinculoModel
from app.repositories.denuncia_repository import converter_object_id


class VinculoRepository:
    def __init__(self, database: Database) -> None:
        self.collection = database.vinculos

    def create(self,denuncia_id: str,data: dict[str, Any],) -> VinculoModel:
        document: VinculoModel = {
            **data,
            "denuncia_id": ObjectId(denuncia_id),
            "encaminhado_em": datetime.now(timezone.utc),
        }
        result = self.collection.insert_one(document)
        return self.collection.find_one({"_id": result.inserted_id})

    def get_by_id(self, vinculo_id: str) -> VinculoModel | None:
        object_id = converter_object_id(vinculo_id)
        if not object_id:
            return None
        return self.collection.find_one({"_id": object_id})

    def get_by_orgao(self,denuncia_id: str,orgao_nome_normalizado: str,) -> VinculoModel | None:
        object_id = converter_object_id(denuncia_id)
        if not object_id:
            return None
        return self.collection.find_one(
            {
                "denuncia_id": object_id,
                "orgao_nome_normalizado": orgao_nome_normalizado,
            }
        )

    def list_by_denuncia(self, denuncia_id: str) -> list[VinculoModel]:
        object_id = converter_object_id(denuncia_id)
        if not object_id:
            return []
        return list(
            self.collection.find({"denuncia_id": object_id}).sort(
                "encaminhado_em",
                DESCENDING,
            )
        )

    def count_by_denuncia(self, denuncia_id: str) -> int:
        object_id = converter_object_id(denuncia_id)
        if not object_id:
            return 0
        return self.collection.count_documents({"denuncia_id": object_id})

    def update(self,vinculo_id: str,data: dict[str, Any],
    ) -> VinculoModel | None:
        object_id = converter_object_id(vinculo_id)
        if not object_id:
            return None
        self.collection.update_one({"_id": object_id}, {"$set": data})
        return self.collection.find_one({"_id": object_id})

    def delete(self, vinculo_id: str) -> bool:
        object_id = converter_object_id(vinculo_id)
        if not object_id:
            return False
        return self.collection.delete_one({"_id": object_id}).deleted_count == 1

    def delete_by_denuncia(self, denuncia_id: str) -> int:
        object_id = converter_object_id(denuncia_id)
        if not object_id:
            return 0
        return self.collection.delete_many({"denuncia_id": object_id}).deleted_count
