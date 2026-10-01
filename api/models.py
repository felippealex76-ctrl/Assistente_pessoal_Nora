from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class TarefaEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    prioridade: Literal["alta", "media", "baixa"] = "media"

class TarefaAtualizar(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    prioridade: Literal["alta", "media", "baixa"]
    concluida: bool

class NotaEntrada(BaseModel):
    conteudo: str = Field(min_length=1)

class CompromissoEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    data_hora: datetime
    local: str | None = None