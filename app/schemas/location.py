from datetime import datetime

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator


class LocalCreate(BaseModel):
    nome: str = Field(min_length=3, max_length=120)
    bairro: str = Field(min_length=2, max_length=100)
    cidade: str = Field(min_length=2, max_length=100)
    uf: str = Field(min_length=2, max_length=2)
    referencia: str | None = Field(default=None, max_length=200)

    @field_validator("uf")
    @classmethod
    def normalizar_uf(cls, value: str) -> str:
        return value.upper()

    @field_validator("nome", "bairro", "cidade")
    @classmethod
    def remover_espacos_externos(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O texto não pode conter apenas espaços.")
        return value


class LocalResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(validation_alias=AliasChoices("_id", "id"))
    nome: str
    bairro: str
    cidade: str
    uf: str
    referencia: str | None
    criado_em: datetime

    @field_validator("id", mode="before")
    @classmethod
    def converter_id_para_string(cls, value) -> str:
        return str(value)


class LocalListResponse(BaseModel):
    items: list[LocalResponse]
    total: int
