from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId

from app.enums.prioridade import PrioridadeEnum
from app.enums.status import StatusDenuncia
from app.enums.tipo import TipoEnum


class DenunciaModel(TypedDict):
    _id: NotRequired[ObjectId]
    descricao: str
    tipo: TipoEnum
    prioridade: PrioridadeEnum
    status: StatusDenuncia
    endereco: str
    criado_em: datetime
