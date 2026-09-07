from enum import Enum


class StatusDenuncia(str, Enum):
    REGISTRADA = "registrada"
    EM_ANALISE = "em_analise"
    ENCAMINHADA = "encaminhada"
    RESOLVIDA = "resolvida"
    ARQUIVADA = "arquivada"
