from enum import Enum


class PrioridadeEnum(str, Enum):
    BAIXA = 'baixa'
    MEDIA = 'media'
    ALTA = 'alta'
    URGENTE = 'urgente'
