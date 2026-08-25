class DenunciaRepository:
    def criar(self, denuncia: DenunciaRequestEntity) -> DenunciaResponseEntity:
        ...

    def buscar_por_id(self, id: int) -> DenunciaResponseEntity | None:
        ...

    def listar(self) -> list[DenunciaResponseEntity]:
        ...

    def atualizar_vinculo(
        self,
        id: int,
        vinculo: VinculoEntity
    ) -> DenunciaResponseEntity:
        ...
