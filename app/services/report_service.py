from typing import Any

from app.entities.report import DenunciaModel
from app.enums.priority import PrioridadeEnum
from app.enums.status import StatusDenuncia
from app.enums.report_type import TipoEnum
from app.exceptions import BusinessRuleError, NotFoundError
from app.repositories.report_repository import DenunciaRepository
from app.repositories.location_repository import LocalRepository
from app.schemas.report import DenunciaCreate, DenunciaUpdate


class DenunciaService:
    def __init__(
        self,
        repository: DenunciaRepository,
        locais: LocalRepository | None = None,
    ) -> None:
        self.repository = repository
        self.locais = locais

    def _validar_local(self, local_id: str | None) -> None:
        if local_id and self.locais and not self.locais.get_by_id(local_id):
            raise BusinessRuleError(f"Local {local_id} não existe.")

    def create(self, payload: DenunciaCreate) -> DenunciaModel:
        self._validar_local(payload.local_id)
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
        local_id: str | None = None,
        limit: int,
        offset: int,
    ) -> tuple[list[DenunciaModel], int]:
        return self.repository.list(
            tipo=tipo,
            prioridade=prioridade,
            local_id=local_id,
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
        observacao = data.pop("observacao", None)
        self._validar_local(data.get("local_id"))

        historico = None
        novo_status = data.get("status")
        if novo_status and novo_status != denuncia["status"]:
            historico = {
                "status_anterior": denuncia["status"],
                "status_novo": novo_status,
                "observacao": observacao or "Status atualizado.",
            }

        if historico:
            atualizada = self.repository.update(denuncia_id, data, historico)
        else:
            atualizada = self.repository.update(denuncia_id, data)
        if not atualizada:
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")
        return atualizada

    def delete(self, denuncia_id: str) -> None:
        if not self.repository.get_by_id(denuncia_id):
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")
        if not self.repository.delete(denuncia_id):
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")
