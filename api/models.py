from pydantic import BaseModel, Field
from typing import Literal


class TarefaEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    prioridade: Literal["alta", "media", "baixa"] = "media"

class TarefaAtualizar(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    prioridade: Literal["alta", "media", "baixa"]
    concluida: bool

class NotaEntrada(BaseModel):
    conteudo: str = Field(min_length=1)
