from datetime import datetime, timezone
from typing import Any

from pymongo import ASCENDING
from pymongo.database import Database

from app.entities.location import LocalModel
from app.repositories.report_repository import converter_object_id


class LocalRepository:
    def __init__(self, database: Database) -> None:
        self.collection = database.locais
        self.denuncias = database.denuncias

    def create(self, data: dict[str, Any]) -> LocalModel:
        document = {**data, "criado_em": datetime.now(timezone.utc)}
        result = self.collection.insert_one(document)
        return self.collection.find_one({"_id": result.inserted_id})

    def get_by_id(self, local_id: str) -> LocalModel | None:
        object_id = converter_object_id(local_id)
        if not object_id:
            return None
        return self.collection.find_one({"_id": object_id})

    def list(self) -> list[LocalModel]:
        return list(self.collection.find().sort("nome", ASCENDING))

    def has_denuncias(self, local_id: str) -> bool:
        return self.denuncias.count_documents({"local_id": local_id}) > 0

    def delete(self, local_id: str) -> bool:
        object_id = converter_object_id(local_id)
        if not object_id:
            return False
        return self.collection.delete_one({"_id": object_id}).deleted_count == 1
