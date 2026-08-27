from datetime import datetime

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class VinculoCreate(BaseModel):
    orgao_nome: str = Field(min_length=2, max_length=160)
    orgao_tipo: str | None = Field(default=None, max_length=80)
    contato: str | None = Field(default=None, max_length=160)
    protocolo: str | None = Field(default=None, max_length=80)
    observacoes: str | None = Field(default=None, max_length=1000)

    @field_validator("orgao_nome")
    @classmethod
    def normalizar_orgao(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("O nome do órgão deve ter ao menos 2 caracteres.")
        return value


class VinculoUpdate(BaseModel):
    orgao_nome: str | None = Field(default=None, min_length=2, max_length=160)
    orgao_tipo: str | None = Field(default=None, max_length=80)
    contato: str | None = Field(default=None, max_length=160)
    protocolo: str | None = Field(default=None, max_length=80)
    observacoes: str | None = Field(default=None, max_length=1000)

    @field_validator("orgao_nome")
    @classmethod
    def normalizar_orgao(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if len(value) < 2:
            raise ValueError("O nome do órgão deve ter ao menos 2 caracteres.")
        return value

    @model_validator(mode="after")
    def validar_atualizacao(self):
        if not self.model_fields_set:
            raise ValueError("Informe ao menos um campo para atualizar.")
        if "orgao_nome" in self.model_fields_set and self.orgao_nome is None:
            raise ValueError("orgao_nome não pode ser nulo.")
        return self


class VinculoResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(validation_alias=AliasChoices("_id", "id"))
    denuncia_id: str
    orgao_nome: str
    orgao_tipo: str | None
    contato: str | None
    protocolo: str | None
    observacoes: str | None
    encaminhado_em: datetime

    @field_validator("id", "denuncia_id", mode="before")
    @classmethod
    def converter_ids_para_string(cls, value) -> str:
        return str(value)
