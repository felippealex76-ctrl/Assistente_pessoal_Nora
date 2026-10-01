from fastapi import FastAPI, HTTPException
from db import conectar
from models import TarefaEntrada
from models import TarefaEntrada, TarefaAtualizar

app = FastAPI(title="Nora API")


@app.get("/")
def raiz():
    return {"mensagem": "Nora esta no ar!"}

@app.get("/tarefas")
def listar_tarefas():

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT id, titulo, concluida, prioridade FROM tarefas")
        linhas = cursor.fetchall()
        conexao.close()

        tarefas = []
        for linha in linhas:
            tarefas.append({
                "id": linha.id,
                "titulo": linha.titulo,
                "concluida": bool(linha.concluida),
                "prioridade": linha.prioridade,
            })
        return tarefas

@app.post("/tarefas")
def criar_tarefa(tarefa: TarefaEntrada):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO tarefas (titulo, prioridade) OUTPUT INSERTED.id VALUES (?, ?)",
        tarefa.titulo, tarefa.prioridade,
    )
    novo_id = cursor.fetchone()[0]
    conexao.commit()
    conexao.close()
    return {
        "id": novo_id,
        "titulo": tarefa.titulo,
        "concluida": False,
        "prioridade": tarefa.prioridade,
    }

@app.get("/tarefas/{id}")
def obter_tarefa(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, titulo, concluida, prioridade FROM tarefas WHERE id = ?", 
        id,
    )

    linha = cursor.fetchone()
    conexao.close()

    if linha is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {
        "id": linha.id,
        "titulo": linha.titulo,
        "concluida": bool(linha.concluida),
        "prioridade": linha.prioridade,
    }

@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, tarefa: TarefaAtualizar):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE tarefas SET titulo = ?, prioridade = ?, concluida = ? WHERE id = ?",
        tarefa.titulo, tarefa.prioridade, tarefa.concluida, id, 
    )
    afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()

    if afetadas == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    return {
        "id": id,
        "titulo": tarefa.titulo,
        "prioridade": tarefa.prioridade,
        "concluida": tarefa.concluida,
    }
@app.delete("/tarefas/{id}")
def apagar_tarefa(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", id)
    afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()
    if afetadas == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

        return {"mensagem": f"Tarefa {id} apagada com sucesso"}