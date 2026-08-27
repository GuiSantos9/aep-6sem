from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId


class VinculoModel(TypedDict):
    """Formato persistido na coleção `vinculos`."""

    _id: NotRequired[ObjectId]
    denuncia_id: ObjectId
    orgao_nome: str
    orgao_nome_normalizado: str
    orgao_tipo: str | None
    contato: str | None
    protocolo: str | None
    observacoes: str | None
    encaminhado_em: datetime

