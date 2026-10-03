import requests
from datetime import datetime
from voz import falar, falar_interrompivel
from escuta import ouvir
from brain import interpretar

API = "http://127.0.0.1:8000"


# ---------------------------------------------------------------- TAREFAS
def criar_tarefa(titulo):
    try:
        resposta = requests.post(f"{API}/tarefas", json={"titulo": titulo})
    except requests.exceptions.ConnectionError:
        falar("Não consegui falar com o servidor. Ele está ligado?")
        return

    if resposta.status_code == 200:
        falar(f"Pronto! Anotei a tarefa: {titulo}")
    else:
        print("[API] ERRO AO CRIAR:", resposta.status_code, resposta.text)
        falar("Ops, não consegui criar a tarefa.")


def listar_tarefas():
    try:
        resposta = requests.get(f"{API}/tarefas")
    except requests.exceptions.ConnectionError:
        falar("Não consegui falar com o servidor. Ele está ligado?")
        return

    tarefas = resposta.json()
    if not tarefas:
        falar("Você não tem nenhuma tarefa por enquanto.")
        return
    falar(f"Você tem {len(tarefas)} tarefas.")
    for tarefa in tarefas:
        falar(tarefa["titulo"])


def _achar_tarefa(tarefas, texto):
    """Devolve a tarefa que mais combina com o texto falado (ou None)."""
    palavras = texto.lower().split()
    melhor = None
    melhor_pontos = 0
    for tarefa in tarefas:
        titulo = tarefa["titulo"].lower()
        pontos = sum(1 for palavra in palavras if palavra in titulo)
        if pontos > melhor_pontos:
            melhor_pontos = pontos
            melhor = tarefa
    return melhor


def concluir_tarefa(texto):
    try:
        resposta = requests.get(f"{API}/tarefas")
    except requests.exceptions.ConnectionError:
        falar("Não consegui falar com o servidor. Ele está ligado?")
        return

    tarefas = resposta.json()
    pendentes = [t for t in tarefas if not t["concluida"]]
    tarefa = _achar_tarefa(pendentes, texto)

    if tarefa is None:
        falar("Não encontrei nenhuma tarefa parecida com isso.")
        return

    corpo = {
        "titulo": tarefa["titulo"],
        "prioridade": tarefa["prioridade"],
        "concluida": True,
    }
    resposta = requests.put(f"{API}/tarefas/{tarefa['id']}", json=corpo)

    if resposta.status_code == 200:
        falar(f"Feito! Marquei como concluída: {tarefa['titulo']}")
    else:
        print("[API] ERRO AO CONCLUIR:", resposta.status_code, resposta.text)
        falar("Ops, não consegui concluir a tarefa.")


def apagar_tarefa(texto):
    try:
        resposta = requests.get(f"{API}/tarefas")
    except requests.exceptions.ConnectionError:
        falar("Não consegui falar com o servidor. Ele está ligado?")
        return

    tarefas = resposta.json()
    tarefa = _achar_tarefa(tarefas, texto)

    if tarefa is None:
        falar("Não encontrei nenhuma tarefa parecida com isso.")
        return

    falar(f"Quer mesmo apagar a tarefa: {tarefa['titulo']}?.")
    confirmacao = ouvir()
    print("[CONFIRMA] ouvi:", repr(confirmacao))

    if not confirmacao or "sim" not in confirmacao.lower():
        falar("Tudo bem, não apaguei nada.")
        return

    resposta = requests.delete(f"{API}/tarefas/{tarefa['id']}")

    if resposta.status_code == 200:
        falar(f"Pronto, apaguei a tarefa: {tarefa['titulo']}")
    else:
        print("[API] ERRO AO APAGAR:", resposta.status_code, resposta.text)
        falar("Ops, não consegui apagar a tarefa.")


# ---------------------------------------------------------------- NOTAS
def criar_nota(conteudo):
    try:
        resposta = requests.post(f"{API}/notas", json={"conteudo": conteudo})
    except requests.exceptions.ConnectionError:
        falar("Não consegui falar com o servidor. Ele está ligado?")
        return

    if resposta.status_code == 200:
        falar("Anotei nas suas notas.")
    else:
        print("[API] ERRO AO CRIAR NOTA:", resposta.status_code, resposta.text)
        falar("Ops, não consegui salvar a nota.")


def listar_notas():
    try:
        resposta = requests.get(f"{API}/notas")
    except requests.exceptions.ConnectionError:
        falar("Não consegui falar com o servidor. Ele está ligado?")
        return

    notas = resposta.json()
    if not notas:
        falar("Você não tem nenhuma nota.")
        return
    falar(f"Você tem {len(notas)} notas.")
    for nota in notas:
        falar(nota["conteudo"])


# ---------------------------------------------------------------- COMPROMISSOS
def _formatar_data(iso):
    """Transforma '2026-10-03T15:00:00' em algo falável: '03/10 às 15:00'."""
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%d/%m às %H:%M")
    except (ValueError, TypeError):
        return iso


def criar_compromisso(titulo, data_hora, local):
    corpo = {"titulo": titulo, "data_hora": data_hora}
    if local:
        corpo["local"] = local
    try:
        resposta = requests.post(f"{API}/compromissos", json=corpo)
    except requests.exceptions.ConnectionError:
        falar("Não consegui falar com o servidor. Ele está ligado?")
        return

    if resposta.status_code == 200:
        quando = _formatar_data(data_hora)
        falar(f"Agendado: {titulo}, {quando}.")
    else:
        print("[API] ERRO AO AGENDAR:", resposta.status_code, resposta.text)
        falar("Ops, não consegui agendar o compromisso.")


def listar_compromissos():
    try:
        resposta = requests.get(f"{API}/compromissos")
    except requests.exceptions.ConnectionError:
        falar("Não consegui falar com o servidor. Ele está ligado?")
        return

    compromissos = resposta.json()
    if not compromissos:
        falar("Você não tem compromissos agendados.")
        return
    falar(f"Você tem {len(compromissos)} compromissos.")
    for comp in compromissos:
        quando = _formatar_data(comp["data_hora"])
        falar(f"{comp['titulo']}, {quando}")


# ---------------------------------------------------------------- DESPACHANTE
def processar(comando):
    if not comando:
        return

    decisao = interpretar(comando)
    print("[CEREBRO] decisao:", decisao)
    acao = decisao.get("acao")

    if acao == "criar_tarefa":
        titulo = decisao.get("titulo", "").strip()
        if titulo:
            criar_tarefa(titulo)
        else:
            falar("Qual é o título da tarefa?")
    elif acao == "listar_tarefas":
        listar_tarefas()
    elif acao == "concluir_tarefa":
        titulo = decisao.get("titulo", "").strip()
        if titulo:
            concluir_tarefa(titulo)
        else:
            falar("Qual tarefa você quer concluir?")
    elif acao == "apagar_tarefa":
        titulo = decisao.get("titulo", "").strip()
        if titulo:
            apagar_tarefa(titulo)
        else:
            falar("Qual tarefa você quer apagar?")
    elif acao == "criar_nota":
        conteudo = decisao.get("conteudo", "").strip()
        if conteudo:
            criar_nota(conteudo)
        else:
            falar("O que você quer que eu anote?")
    elif acao == "listar_notas":
        listar_notas()
    elif acao == "criar_compromisso":
        titulo = decisao.get("titulo", "").strip()
        data_hora = decisao.get("data_hora", "").strip()
        local = decisao.get("local", "").strip()
        if titulo and data_hora:
            criar_compromisso(titulo, data_hora, local)
        else:
            falar("Qual é o compromisso e para quando?")
    elif acao == "listar_compromissos":
        listar_compromissos()

    elif acao == "conversar":
            falar_interrompivel(decisao.get("resposta",""))
    else:
            falar(decisao.get("resposta") or "Ainda não sei fazer isso, mas estou aprendendo!")
    
        
        

    
if __name__ == "__main__":
    print("[NORA] iniciando...")
    falar("Oi! Estou aqui. pode falar.")
    while True:
        comando = ouvir()
        print("[ESCUTA] ouvi:", repr(comando))
        if comando and ("sair" in comando.lower() or "tchau" in comando.lower()):
            falar("Até logo!")
            break
        processar(comando)
