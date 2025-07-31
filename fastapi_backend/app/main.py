# /fastapi_backend/app/main.py
# v1.2 - 2025-07-30 13:20:00 - Refatoração leve, comentários claros, base opcional ativável via env.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import (
    auth,
    users,
    recados,
    agenda,
    historia,
    galeria,
    repertorio
)

import os

# === ⚙️ Configuração da aplicação ===
app = FastAPI(
    title="Setor Musical MS API",
    description="API para o sistema de gerenciamento do Setor Musical.",
    version="1.0.0"
)

# === 🌐 CORS: Ajuste aqui conforme os domínios do frontend ===
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://setormusicalms.art.br",  # Produção
    "https://setormusicalms.art.br",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 🛠️ Criação das tabelas (ativar por variável de ambiente) ===
if os.getenv("CREATE_TABLES_ON_STARTUP") == "1":
    Base.metadata.create_all(bind=engine)

# === 🔀 Registro dos roteadores ===
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(recados.router, prefix="/api/recados", tags=["recados"])
app.include_router(agenda.router, prefix="/api/agenda", tags=["agenda"])
app.include_router(historia.router, prefix="/api/historia", tags=["historia"])
app.include_router(galeria.router, prefix="/api/galeria", tags=["galeria"])
app.include_router(repertorio.router, prefix="/api/repertorio", tags=["repertorio"])

# === 🧪 Health check ===
@app.get("/api/health", tags=["Health Check"])
def health_check():
    return {"status": "ok"}

# === 📢 Endpoint raiz ===
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bem-vindo à API do Setor Musical MS"}
