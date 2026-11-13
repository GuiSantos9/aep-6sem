from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId

from app.enums.priority import PrioridadeEnum
from app.enums.status import StatusDenuncia
from app.enums.report_type import TipoEnum


class HistoricoModel(TypedDict):
    """Subdocumento aninhado: uma mudança de status da denúncia."""

    status_anterior: StatusDenuncia | None
    status_novo: StatusDenuncia
    observacao: str
    data: datetime


class DenunciaModel(TypedDict):
    _id: NotRequired[ObjectId]
    descricao: str
    tipo: TipoEnum
    prioridade: PrioridadeEnum
    status: StatusDenuncia
    endereco: str
    criado_em: datetime
    local_id: NotRequired[str | None]
    historico: NotRequired[list[HistoricoModel]]
