class DenunciaRequestEntity:
    descricao: str
    tipo: TipoEnum
    endereco: str
    telefone: str
    prioridade: PrioridadeEnum

class DenunciaResponseEntity:
    id: int
    descricao: str
    tipo: TipoEnum
    endereco: str
    telefone: str
    prioridade: PrioridadeEnum
    vinculo: VinculoEntity | None

class VinculoEntity:
    orgao: str
    data: datetime
    justificativa: str
