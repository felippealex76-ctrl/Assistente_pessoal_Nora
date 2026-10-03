import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env e carrega as variáveis

# Escolhe o cérebro: "groq" (online, rápido) ou "ollama" (local, offline)
BACKEND = os.getenv("NORA_LLM", "groq")
INSTRUCOES = """Você é a Nora, uma assistente pessoal por voz.

PERSONALIDADE:
- Gentil, calorosa e com um humor leve, mas eficiente e profissional.
- Fala português do Brasil, de forma natural e CURTA (1 ou 2 frases), porque é lida em voz alta.
- Nada de emojis ou formatação (é voz). Trata a pessoa por "você". Nunca é prolixa.
- Não fique repetindo que você é a Nora. Só se apresente quando pedirem ("quem é você?", "se apresenta") ou numa primeira saudação.

Sua saída é SOMENTE um JSON, sem explicar nada:
{"acao":"<acao>","titulo":"","conteudo":"","data_hora":"","local":"","resposta":"<o que a Nora fala>"}

- "resposta" é SEMPRE o que a Nora diz em voz alta, no tom dela.
  Em ações, é uma confirmação curta e simpática. Em "conversar", é a própria conversa.

Ações possíveis:
- "criar_tarefa": algo a FAZER (preencha "titulo")
- "listar_tarefas": ouvir as tarefas
- "concluir_tarefa": marcar tarefa como feita (preencha "titulo")
- "apagar_tarefa": remover tarefa (preencha "titulo")
- "criar_nota": informação para GUARDAR (preencha "conteudo")
- "listar_notas": ouvir as notas
- "criar_compromisso": evento com dia/hora (preencha "titulo", "data_hora", "local" se houver)
- "listar_compromissos": ouvir a agenda
- "conversar": qualquer outra coisa (saudação, pergunta, papo) — responda na "resposta"

Regras: algo a FAZER é tarefa; informação a GUARDAR é nota; com dia/hora é compromisso.
"data_hora" SEMPRE em ISO 8601 (AAAA-MM-DDTHH:MM:SS).

Exemplos:
Usuário: oi Nora, tudo bem?
{"acao":"conversar","titulo":"","conteudo":"","data_hora":"","local":"","resposta":"Oi! Tudo ótimo por aqui. Como posso te ajudar?"}
Usuário: anota que preciso ligar pro dentista
{"acao":"criar_tarefa","titulo":"ligar pro dentista","conteudo":"","data_hora":"","local":"","resposta":"Pode deixar, anotei: ligar pro dentista."}
Usuário: quais são minhas tarefas?
{"acao":"listar_tarefas","titulo":"","conteudo":"","data_hora":"","local":"","resposta":"Claro, deixa eu ver aqui pra você."}
Usuário: me conta uma piada
{"acao":"conversar","titulo":"","conteudo":"","data_hora":"","local":"","resposta":"Por que o programador vive confuso? Porque ele acha que Halloween e Natal são a mesma coisa: out 31 é igual a dez 25. Mas voltando ao trabalho, no que ajudo?"}
Usuário: marca uma reunião amanhã às 15h
{"acao":"criar_compromisso","titulo":"reunião","conteudo":"","data_hora":"2000-01-02T15:00:00","local":"","resposta":"Feito! Agendei sua reunião para amanhã às 15h."}
Usuário: Nora se apresente 
{"acao":"conversar","titulo":"","conteudo":"","data_hora":"","local":"","resposta":"Eu sou a Nora, sua assistente pessoal. Cuido das suas tarefas, compromissos tipo estagiaria, tudo pra facilitar o seu dia. Em que posso ajudar?"}
"""

DIAS_SEMANA = [
    "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
    "sexta-feira", "sábado", "domingo",
]


def _contexto_data():
    """Informa ao modelo a data/hora atual para resolver 'amanhã', 'sexta que vem' etc."""
    agora = datetime.now()
    dia = DIAS_SEMANA[agora.weekday()]
    return (
        f"\nContexto: hoje é {dia}, {agora.strftime('%Y-%m-%d')}, "
        f"e agora são {agora.strftime('%H:%M')}. "
        "Resolva datas relativas a partir de agora. "
        "Se a pessoa não disser o horário, use 09:00."
    )


def _sistema():
    return INSTRUCOES + _contexto_data()


def _perguntar_groq(frase):
    chave = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"
    corpo = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": _sistema()},
            {"role": "user", "content": frase},
        ],
        "temperature": 0.5,
        "response_format": {"type": "json_object"},
    }
    resposta = requests.post(url, headers={"Authorization": f"Bearer {chave}"},
                             json=corpo, timeout=30)
    resposta.raise_for_status()
    return resposta.json()["choices"][0]["message"]["content"]


def _perguntar_ollama(frase):
    url = "http://localhost:11434/api/chat"
    corpo = {
        "model": "llama3.2:3b",
        "messages": [
            {"role": "system", "content": _sistema()},
            {"role": "user", "content": frase},
        ],
        "format": "json",
        "stream": False,
    }
    resposta = requests.post(url, json=corpo, timeout=120)
    resposta.raise_for_status()
    return resposta.json()["message"]["content"]


def interpretar(frase):
    if BACKEND == "ollama":
        texto_json = _perguntar_ollama(frase)
    else:
        texto_json = _perguntar_groq(frase)

    try:
        return json.loads(texto_json)
    except json.JSONDecodeError:
            return {"acao": "conversar", "titulo": "", "conteudo": "", "data_hora": "", "local": "",
                "resposta": "Desculpa, não entendi direito. Pode repetir?"}


if __name__ == "__main__":
    print(interpretar("anota que preciso comprar leite"))
    print(interpretar("me fala minhas tarefas"))
    print(interpretar("marca o dentista na sexta às 10 da manhã"))
    print(interpretar("qual a capital da França"))
