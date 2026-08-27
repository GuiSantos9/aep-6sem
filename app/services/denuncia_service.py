from typing import Any

from app.entities.denuncia import DenunciaModel
from app.enums.prioridade import PrioridadeEnum
from app.enums.status import StatusDenuncia
from app.enums.tipo import TipoArquiteturaHostil
from app.exceptions import BusinessRuleError, NotFoundError
from app.repositories.denuncia_repository import DenunciaRepository
from app.repositories.vinculo_repository import VinculoRepository
from app.schemas.denuncia import DenunciaCreate, DenunciaUpdate


class DenunciaService:
    def __init__(
        self,
        repository: DenunciaRepository,
        vinculo_repository: VinculoRepository,
    ) -> None:
        self.repository = repository
        self.vinculo_repository = vinculo_repository

    @staticmethod
    def _validar_coordenadas(
        latitude: float | None,
        longitude: float | None,
    ) -> None:
        if (latitude is None) != (longitude is None):
            raise BusinessRuleError(
                "Latitude e longitude devem ser informadas juntas."
            )

    def create(self, payload: DenunciaCreate) -> DenunciaModel:
        self._validar_coordenadas(payload.latitude, payload.longitude)
        data = payload.model_dump(mode="json")
        data["status"] = StatusDenuncia.registrada.value
        return self.repository.create(data)

    def get(self, denuncia_id: str) -> dict[str, Any]:
        denuncia = self.repository.get_by_id(denuncia_id)
        if not denuncia:
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")

        resposta = dict(denuncia)
        resposta["vinculos"] = self.vinculo_repository.list_by_denuncia(
            denuncia_id
        )
        return resposta

    def list(
        self,
        *,
        tipo: TipoArquiteturaHostil | None,
        prioridade: PrioridadeEnum | None,
        status: StatusDenuncia | None,
        cidade: str | None,
        bairro: str | None,
        orgao_nome: str | None,
        busca: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[DenunciaModel], int]:
        return self.repository.list(
            tipo=tipo,
            prioridade=prioridade,
            status=status,
            cidade=cidade,
            bairro=bairro,
            orgao_nome=orgao_nome,
            busca=busca,
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
        latitude = data.get("latitude", denuncia.get("latitude"))
        longitude = data.get("longitude", denuncia.get("longitude"))
        self._validar_coordenadas(latitude, longitude)

        if (
            data.get("status") == StatusDenuncia.encaminhada.value
            and self.vinculo_repository.count_by_denuncia(denuncia_id) == 0
        ):
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

        self.vinculo_repository.delete_by_denuncia(denuncia_id)
        if not self.repository.delete(denuncia_id):
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")

