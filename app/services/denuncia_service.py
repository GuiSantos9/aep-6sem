from typing import Any

from app.entities.denuncia import DenunciaModel
from app.enums.prioridade import PrioridadeEnum
from app.enums.status import StatusDenuncia
from app.enums.tipo import TipoEnum
from app.exceptions import BusinessRuleError, NotFoundError
from app.repositories.denuncia_repository import DenunciaRepository
from app.schemas.denuncia import DenunciaCreate, DenunciaUpdate


class DenunciaService:
    def __init__(self, repository: DenunciaRepository) -> None:
        self.repository = repository

    def create(self, payload: DenunciaCreate) -> DenunciaModel:
        data = payload.model_dump(mode="json")
        data["status"] = StatusDenuncia.REGISTRADA
        return self.repository.create(data)

    def get(self, denuncia_id: str) -> dict[str, Any]:
        denuncia = self.repository.get_by_id(denuncia_id)
        if not denuncia:
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")
        return dict(denuncia)

    def list(
        self,
        *,
        tipo: TipoEnum | None,
        prioridade: PrioridadeEnum | None,
        orgao_nome: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[DenunciaModel], int]:
        return self.repository.list(
            tipo=tipo,
            prioridade=prioridade,
            orgao_nome=orgao_nome,
            limit=limit,
            offset=offset,
        )

    def update(
        self,
        denuncia_id: str,
        payload: DenunciaUpdate,
    ) -> DenunciaModel:
        denuncia = self.repository.get_by_id(denuncia_id)
        if not denuncia:
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")

        data = payload.model_dump(exclude_unset=True, mode="json")

        if data.get("status") == StatusDenuncia.ENCAMINHADA:
            if not denuncia.get("vinculos"):
                raise BusinessRuleError(
                    "A denúncia precisa de um vínculo antes de ser encaminhada."
                )

        atualizada = self.repository.update(denuncia_id, data)
        if not atualizada:
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")
        return atualizada

    def delete(self, denuncia_id: str) -> None:
        if not self.repository.get_by_id(denuncia_id):
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")
        if not self.repository.delete(denuncia_id):
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")
