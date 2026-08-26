from enums.tipo import TipoEnum
from enums.prioridade import PrioridadeEnum
from .vinculo import VinculoEntity
from pydantic import BaseModel


class DenunciaRequestEntity(BaseModel):
    descricao: str
    tipo: TipoEnum
    endereco: str
    telefone: str
    prioridade: PrioridadeEnum


class DenunciaResponseEntity(DenunciaRequestEntity):
    id: int
    descricao: str
    tipo: TipoEnum
    endereco: str
    telefone: str
    prioridade: PrioridadeEnum
    vinculo: VinculoEntity | None
