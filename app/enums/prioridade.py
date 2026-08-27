from enum import Enum


class PrioridadeEnum(str, Enum):
    BAIXA = 'BAIXA'
    MEDIA = 'MEDIA'
    ALTA = 'ALTA'
    URGENTE = 'URGENTE'
