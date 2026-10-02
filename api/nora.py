import requests 
from voz import falar 
from escuta import ouvir

API = "http://127.0.0.1:8000"

def criar_tarefa(titulo):
    resposta = requests.post(f"{API}/tarefas", json={"titulo": titulo})
    if resposta.status_code == 200:
        falar(f"Pronto! Anotei a tarefa: {titulo}")
    else:
        falar("Ops, não consegui criar a tarefa.")



def listar_tarefas():
    resposta = requests.get(f"{API}/tarefas")
    tarefas = resposta.json()
    if not tarefas:
        falar("você não tem nenhuma tarefa por enquanto.")
        return
    falar(f"você tem {len(tarefas)} tarefas.")
    for tarefa in tarefas:
        falar(tarefa["titulo"])


def processar(comando):
    comando = comando.lower()

    if comando.startswith("criar tarefa"):
        titulo = comando.replace("criar tarefa", "").strip()
        if titulo:
            criar_tarefa(titulo)
        else:
            falar("Qual é o título da tarefa?")
    elif "listar tarefas" in comando or "minhas tarefas" in comando:
        listar_tarefas()
    elif comando == "":
        pass  # não entendeu nada, só ignora
    else:
        falar("Ainda não sei fazer isso, mas estou aprendendo!")

if __name__ == "__main__":
    falar("Olá! Eu sou a Nora. Pode falar seu comando. Diga 'sair' quando quiser parar.")
    while True:
        comando = ouvir()
        if comando and ("sair" in comando.lower() or "tchau" in comando.lower()):
            falar("Até logo!")
            break
        processar(comando)
