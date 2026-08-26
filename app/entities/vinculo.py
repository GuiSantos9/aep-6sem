from datetime import date
from pydantic import BaseModel


class VinculoEntity(BaseModel):
    orgao: str
    data: date
    justificativa: str
