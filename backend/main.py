# setormusicalms\main.py
from fastapi import FastAPI
from routers import auth

app = FastAPI(
    title="Setor Musical MS",
    description="Microserviço para gerenciar entidades do setor musical.",
    version="1.0.0"
)

# Inclui o roteador de autenticação na aplicação principal
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Setor Musical"}