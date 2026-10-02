from fastapi import FastAPI
from routers import tarefas, notas, compromissos

app = FastAPI(title="Nora API")


@app.get("/")
def raiz():
    return {"mensagem": "Nora esta no ar!"}


app.include_router(tarefas.router)
app.include_router(notas.router)
app.include_router(compromissos.router)