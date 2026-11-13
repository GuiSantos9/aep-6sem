from enum import Enum


class TipoEnum(str, Enum):
    BANCO_DIVIDIDO = "banco_dividido"
    ESPIGAO_METALICO = "espigao_metalico"
    INCLINACAO_DE_SUPERFICIE = "inclinacao_de_superficie"
    RETIRADA_DE_ASSENTO = "retirada_de_assento"
    BARREIRA_FISICA = "barreira_fisica"
    EMISSAO_SONORA = "emissao_sonora"
    ASPERSOR_DE_AGUA = "aspersor_de_agua"
    OUTRO = "outro"
