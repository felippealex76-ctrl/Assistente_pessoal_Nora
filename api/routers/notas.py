from fastapi import APIRouter, HTTPException
from db import conectar
from models import NotaEntrada

router = APIRouter(prefix="/notas", tags=["Notas"])


@router.get("")
def listar_notas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, conteudo, criada_em FROM notas")
    linhas = cursor.fetchall()
    conexao.close()
    notas = []
    for linha in linhas:
        notas.append({"id": linha.id, "conteudo": linha.conteudo, "criada_em": str(linha.criada_em)})
    return notas


@router.post("")
def criar_nota(nota: NotaEntrada):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO notas (conteudo) OUTPUT INSERTED.id VALUES (?)", nota.conteudo)
    novo_id = cursor.fetchone()[0]
    conexao.commit()
    conexao.close()
    return {"id": novo_id, "conteudo": nota.conteudo}


@router.get("/{id}")
def obter_nota(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, conteudo, criada_em FROM notas WHERE id = ?", id)
    linha = cursor.fetchone()
    conexao.close()
    if linha is None:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    return {"id": linha.id, "conteudo": linha.conteudo, "criada_em": str(linha.criada_em)}


@router.put("/{id}")
def atualizar_nota(id: int, nota: NotaEntrada):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE notas SET conteudo = ? WHERE id = ?", nota.conteudo, id)
    afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()
    if afetadas == 0:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    return {"id": id, "conteudo": nota.conteudo}


@router.delete("/{id}")
def apagar_nota(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM notas WHERE id = ?", id)
    afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()
    if afetadas == 0:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    return {"mensagem": f"Nota {id} apagada com sucesso"}
