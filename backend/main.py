# setormusicalms\backend\amain.py

from fastapi import FastAPI
from routers import auth
from database.database import engine, Base
import models.user # Importa o módulo para que o SQLAlchemy o reconheça ao criar as tabelas

# Cria todas as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS",
    description="Microserviço para gerenciar entidades do setor musical.",
    version="1.0.0",
)

# Inclui o roteador de autenticação na aplicação principal
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do Setor Musical"}