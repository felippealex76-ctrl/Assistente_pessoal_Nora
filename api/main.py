from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import tarefas, notas, compromissos

app = FastAPI(title="Nora API")

# Libera o navegador a conversar com a API (útil para a interface web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tarefas.router)
app.include_router(notas.router)
app.include_router(compromissos.router)


@app.get("/")
def raiz():
    return {"nora": "online", "interface": "/app", "docs": "/docs"}


# Serve a interface web (pasta static/index.html) em http://127.0.0.1:8000/app
app.mount("/app", StaticFiles(directory="static", html=True), name="app")
