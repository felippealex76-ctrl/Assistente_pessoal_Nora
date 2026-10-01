from fastapi import FastAPI, HTTPException
from db import conectar
from models import TarefaEntrada, TarefaAtualizar, NotaEntrada

app = FastAPI(title="Nora API")


@app.get("/")
def raiz():
    return {"mensagem": "Nora esta no ar!"}


# -------------------- TAREFAS --------------------

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
    cursor.execute("INSERT INTO tarefas (titulo, prioridade) OUTPUT INSERTED.id VALUES (?, ?)",
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





# -------------------- NOTAS --------------------



@app.get("/notas")
def listar_notas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, conteudo, criada_em FROM notas")
    linhas = cursor.fetchall()
    conexao.close()

    notas = [] 
    for linha in linhas:
        notas.append({
            "id": linha.id,
            "conteudo": linha.conteudo,
            "criada_em": str(linha.criada_em),
        })
    return notas



@app.post("/notas")
def criar_nota(nota: NotaEntrada):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO notas (conteudo) OUTPUT INSERTED.id VALUES (?)",
        nota.conteudo,
    )
    novo_id = cursor.fetchone()[0]
    conexao.commit()
    conexao.close()
    return {"id": novo_id, "conteudo": nota.conteudo}




@app.get("/notas/{id}")
def obter_nota(id: int):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, conteudo, criada_em FROM notas WHERE id = ?", id)
    linha = cursor.fetchone()
    conexao.close()

    if linha is None:
        raise HHTPExceptional(status_code=404, detail="Nota não encontrada")

    return {
        "id": linha.id,
        "conteudo": linha.conteudo,
        "criada_em": str(linha.criada_em),
    }



@app.put("/notas/{id}")                      # /{id} na rota
def atualizar_nota(id: int, nota: NotaEntrada):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE notas SET conteudo = ? WHERE id = ?",   # vírgula no fim
        nota.conteudo, id,                              # dois valores
    )
    afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()

    if afetadas == 0:
        raise HTTPException(status_code=404, detail="Nota não encontrada")

    return {"id": id, "conteudo": nota.conteudo}


@app.delete("/notas/{id}")
def apagar_nota(id: int):                     # só o id
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM notas WHERE id = ?", id)   # notas, não tarefas
    afetadas = cursor.rowcount
    conexao.commit()
    conexao.close()

    if afetadas == 0:
        raise HTTPException(status_code=404, detail="Nota não encontrada")

    return {"mensagem": f"Nota {id} apagada com sucesso"}   # fora do if
