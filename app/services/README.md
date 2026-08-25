class DenunciaService:
    def __init__(self, repository: DenunciaRepository):
        self.repository = repository

    def criar(self, denuncia: DenunciaRequestEntity) -> DenunciaResponseEntity:
        ...

    def buscar_por_id(self, id: int) -> DenunciaResponseEntity | None:
        ...

    def listar(self) -> list[DenunciaResponseEntity]:
        ...

    def vincular(
        self,
        id: int,
        vinculo: VinculoEntity
    ) -> DenunciaResponseEntity:
        ...
