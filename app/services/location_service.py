from app.entities.location import LocalModel
from app.exceptions import ConflictError, NotFoundError
from app.repositories.location_repository import LocalRepository
from app.schemas.location import LocalCreate


class LocalService:
    def __init__(self, repository: LocalRepository) -> None:
        self.repository = repository

    def create(self, payload: LocalCreate) -> LocalModel:
        return self.repository.create(payload.model_dump(mode="json"))

    def get(self, local_id: str) -> LocalModel:
        local = self.repository.get_by_id(local_id)
        if not local:
            raise NotFoundError(f"Local {local_id} não encontrado.")
        return local

    def list(self) -> list[LocalModel]:
        return self.repository.list()

    def delete(self, local_id: str) -> None:
        self.get(local_id)
        if self.repository.has_denuncias(local_id):
            raise ConflictError(
                "Não é possível excluir um local que possui denúncias vinculadas."
            )
        self.repository.delete(local_id)
