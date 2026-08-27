from datetime import datetime

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    field_validator,
    model_validator,
)

from app.enums.prioridade import PrioridadeEnum
from app.enums.status import StatusDenuncia
from app.enums.tipo import TipoArquiteturaHostil
from app.schemas.vinculo import VinculoResponse


class DenunciaBase(BaseModel):
    titulo: str = Field(min_length=5, max_length=120)
    descricao: str = Field(min_length=10, max_length=5000)
    tipo: TipoArquiteturaHostil
    prioridade: PrioridadeEnum = PrioridadeEnum.MEDIA
    logradouro: str = Field(min_length=3, max_length=160)
    numero: str | None = Field(default=None, max_length=20)
    complemento: str | None = Field(default=None, max_length=100)
    bairro: str = Field(min_length=2, max_length=100)
    cidade: str = Field(min_length=2, max_length=100)
    uf: str = Field(min_length=2, max_length=2)
    cep: str | None = Field(default=None, pattern=r"^\d{5}-?\d{3}$")
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    evidencias: list[HttpUrl] = Field(default_factory=list, max_length=10)

    @field_validator("uf")
    @classmethod
    def normalizar_uf(cls, value: str) -> str:
        return value.upper()

    @field_validator("titulo", "descricao", "logradouro", "bairro", "cidade")
    @classmethod
    def remover_espacos_externos(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O texto não pode conter apenas espaços.")
        return value


class DenunciaCreate(DenunciaBase):
    pass


class DenunciaUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=5, max_length=120)
    descricao: str | None = Field(default=None, min_length=10, max_length=5000)
    tipo: TipoArquiteturaHostil | None = None
    prioridade: PrioridadeEnum | None = None
    status: StatusDenuncia | None = None
    logradouro: str | None = Field(default=None, min_length=3, max_length=160)
    numero: str | None = Field(default=None, max_length=20)
    complemento: str | None = Field(default=None, max_length=100)
    bairro: str | None = Field(default=None, min_length=2, max_length=100)
    cidade: str | None = Field(default=None, min_length=2, max_length=100)
    uf: str | None = Field(default=None, min_length=2, max_length=2)
    cep: str | None = Field(default=None, pattern=r"^\d{5}-?\d{3}$")
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    evidencias: list[HttpUrl] | None = Field(default=None, max_length=10)

    @field_validator("uf")
    @classmethod
    def normalizar_uf(cls, value: str | None) -> str | None:
        return value.upper() if value else value

    @field_validator("titulo", "descricao", "logradouro", "bairro", "cidade")
    @classmethod
    def remover_espacos_externos(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("O texto não pode conter apenas espaços.")
        return value

    @model_validator(mode="after")
    def validar_atualizacao(self):
        if not self.model_fields_set:
            raise ValueError("Informe ao menos um campo para atualizar.")

        campos_obrigatorios = {
            "titulo",
            "descricao",
            "tipo",
            "prioridade",
            "status",
            "logradouro",
            "bairro",
            "cidade",
            "uf",
            "evidencias",
        }
        nulos = [
            campo
            for campo in campos_obrigatorios & self.model_fields_set
            if getattr(self, campo) is None
        ]
        if nulos:
            raise ValueError(
                "Estes campos não podem ser nulos: " + ", ".join(sorted(nulos))
            )
        return self


class DenunciaResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(validation_alias=AliasChoices("_id", "id"))
    titulo: str
    descricao: str
    tipo: TipoArquiteturaHostil
    prioridade: PrioridadeEnum
    status: StatusDenuncia
    logradouro: str
    numero: str | None
    complemento: str | None
    bairro: str
    cidade: str
    uf: str
    cep: str | None
    latitude: float | None
    longitude: float | None
    evidencias: list[HttpUrl]
    criado_em: datetime
    atualizado_em: datetime
    vinculos: list[VinculoResponse] = Field(default_factory=list)

    @field_validator("id", mode="before")
    @classmethod
    def converter_id_para_string(cls, value) -> str:
        return str(value)


class DenunciaListResponse(BaseModel):
    items: list[DenunciaResponse]
    total: int
    limit: int
    offset: int
