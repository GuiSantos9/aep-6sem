from pymongo.errors import DuplicateKeyError

from app.entities.denuncia import DenunciaModel
from app.entities.vinculo import VinculoModel
from app.enums.status import StatusDenuncia
from app.exceptions import ConflictError, NotFoundError
from app.repositories.denuncia_repository import (
    DenunciaRepository,
    converter_object_id,
)
from app.repositories.vinculo_repository import VinculoRepository
from app.schemas.vinculo import VinculoCreate, VinculoUpdate


class VinculoService:
    def __init__(
        self,
        vinculo_repository: VinculoRepository,
        denuncia_repository: DenunciaRepository,
    ) -> None:
        self.vinculo_repository = vinculo_repository
        self.denuncia_repository = denuncia_repository

    def _get_denuncia(self, denuncia_id: str) -> DenunciaModel:
        denuncia = self.denuncia_repository.get_by_id(denuncia_id)
        if not denuncia:
            raise NotFoundError(f"Denúncia {denuncia_id} não encontrada.")
        return denuncia

    def _get_vinculo(
        self,
        denuncia_id: str,
        vinculo_id: str,
    ) -> VinculoModel:
        vinculo = self.vinculo_repository.get_by_id(vinculo_id)
        object_id_denuncia = converter_object_id(denuncia_id)
        if not vinculo or vinculo["denuncia_id"] != object_id_denuncia:
            raise NotFoundError(f"Vínculo {vinculo_id} não encontrado.")
        return vinculo

    def create(
        self,
        denuncia_id: str,
        payload: VinculoCreate,
    ) -> VinculoModel:
        denuncia = self._get_denuncia(denuncia_id)
        orgao_normalizado = payload.orgao_nome.strip().casefold()

        if self.vinculo_repository.get_by_orgao(
            denuncia_id,
            orgao_normalizado,
        ):
            raise ConflictError(
                "Esta denúncia já está vinculada ao órgão informado."
            )

        data = payload.model_dump(mode="json")
        data["orgao_nome"] = payload.orgao_nome.strip()
        data["orgao_nome_normalizado"] = orgao_normalizado
        try:
            vinculo = self.vinculo_repository.create(denuncia_id, data)
        except DuplicateKeyError as exc:
            raise ConflictError(
                "Esta denúncia já está vinculada ao órgão informado."
            ) from exc

        if denuncia["status"] in {
            StatusDenuncia.registrada.value,
            StatusDenuncia.em_analise.value,
        }:
            self.denuncia_repository.update(
                denuncia_id,
                {"status": StatusDenuncia.encaminhada.value},
            )
        return vinculo

    def list(self, denuncia_id: str) -> list[VinculoModel]:
        self._get_denuncia(denuncia_id)
        return self.vinculo_repository.list_by_denuncia(denuncia_id)

    def update(
        self,
        denuncia_id: str,
        vinculo_id: str,
        payload: VinculoUpdate,
    ) -> VinculoModel:
        self._get_denuncia(denuncia_id)
        vinculo = self._get_vinculo(denuncia_id, vinculo_id)
        data = payload.model_dump(exclude_unset=True, mode="json")

        novo_orgao = data.get("orgao_nome")
        if novo_orgao:
            novo_orgao = novo_orgao.strip()
            normalizado = novo_orgao.casefold()
            duplicado = self.vinculo_repository.get_by_orgao(
                denuncia_id,
                normalizado,
            )
            if duplicado and duplicado["_id"] != vinculo["_id"]:
                raise ConflictError(
                    "Esta denúncia já está vinculada ao órgão informado."
                )
            data["orgao_nome"] = novo_orgao
            data["orgao_nome_normalizado"] = normalizado

        try:
            atualizado = self.vinculo_repository.update(vinculo_id, data)
        except DuplicateKeyError as exc:
            raise ConflictError(
                "Esta denúncia já está vinculada ao órgão informado."
            ) from exc

        if not atualizado:
            raise NotFoundError(f"Vínculo {vinculo_id} não encontrado.")
        return atualizado

    def delete(self, denuncia_id: str, vinculo_id: str) -> None:
        denuncia = self._get_denuncia(denuncia_id)
        self._get_vinculo(denuncia_id, vinculo_id)

        if not self.vinculo_repository.delete(vinculo_id):
            raise NotFoundError(f"Vínculo {vinculo_id} não encontrado.")

        if (
            denuncia["status"] == StatusDenuncia.encaminhada.value
            and self.vinculo_repository.count_by_denuncia(denuncia_id) == 0
        ):
            self.denuncia_repository.update(
                denuncia_id,
                {"status": StatusDenuncia.em_analise.value},
            )
