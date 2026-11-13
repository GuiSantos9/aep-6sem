from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId


class LocalModel(TypedDict):
    _id: NotRequired[ObjectId]
    nome: str
    bairro: str
    cidade: str
    uf: str
    referencia: str | None
    criado_em: datetime
