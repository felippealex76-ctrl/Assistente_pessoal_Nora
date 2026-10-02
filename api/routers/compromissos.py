from fastapi import APIRouter, HTTPException
from db import conectar
from models import CompromissoEntrada

router = APIRouter(prefix="/compromissos", tags=["Compromissos"])


@router.get("")
def listar_compromissos():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, data_hora, local FROM compromissos ORDER BY data_hora")
    linhas = cursor.fetchall()
    conexao.close()
    compromissos = []
    for linha in linhas:
        compromissos.append({
            "id": linha.id,
            "titulo": linha.titulo,
            "data_hora": str(linha.data_hora),
            "local": linha.local,
        })
    return compromissos


@router.post("")
def criar_compromisso(comp: CompromissoEntrada):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO compromissos (titulo, data_hora, local) OUTPUT INSERTED.id VALUES (?, ?, ?)",
        comp.titulo, comp.data_hora, comp.local,
    )
    novo_id = cursor.fetchone()[0]
    conexao.commit()
    conexao.close()
    return {"id": novo_id, "titulo": comp.titulo, "data_hora": str(comp.data_hora), "local": comp.local}


@router.get("/{id}")
def obter_compromisso(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, titulo, data_hora, local FROM compromissos WHERE id = ?", id)
    linha = cursor.fetchone()
    conexao.close()
    if linha is None:
        raise HTTPException(status_code=404, detail="Compromisso não encontrado")
    return {"id": linha.id, "titulo": linha.titulo, "data_hora": str(linha.data_hora), "local": linha.local}


@router.put("/{id}")
def atualizar_compromisso(id: int, comp: CompromissoEntrada):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE compromissos SET titulo = ?, data_hora = ?, local = ? WHERE id = ?",
        comp.titulo, comp.data_hora, comp.local, id,
    )
    afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()
    if afetadas == 0:
        raise HTTPException(status_code=404, detail="Compromisso não encontrado")
    return {"id": id, "titulo": comp.titulo, "data_hora": str(comp.data_hora), "local": comp.local}


@router.delete("/{id}")
def apagar_compromisso(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM compromissos WHERE id = ?", id)
    afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()
    if afetadas == 0:
        raise HTTPException(status_code=404, detail="Compromisso não encontrado")
    return {"mensagem": f"Compromisso {id} apagado com sucesso"}
