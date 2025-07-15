# \setormusicalms\main.py
from fastapi import FastAPI

app = FastAPI(
    title="Setor Musical MS",
    description="Microserviço para gerenciar entidades do setor musical.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Setor Musical"}