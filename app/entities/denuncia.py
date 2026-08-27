from datetime import datetime
from typing import NotRequired, TypedDict

from bson import ObjectId


class DenunciaModel(TypedDict):
    _id: NotRequired[ObjectId]
    titulo: str
    descricao: str
    tipo: str
    prioridade: str
    status: str
    logradouro: str
    numero: str | None
    complemento: str | None
    bairro: str
    cidade: str
    uf: str
    cep: str | None
    latitude: float | None
    longitude: float | None
    evidencias: list[str]
    criado_em: datetime
    atualizado_em: datetime

