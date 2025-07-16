# setormusicalms/backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# CORREÇÃO: Usando imports relativos para a nova estrutura de pastas
from .database import engine
from .models import agenda, recado, repertorio, user # models está agora dentro de app
from .routers import (
    auth,
    users,
    repertorio as repertorio_router,
    agenda as agenda_router,
    recados as recados_router
)

# Cria as tabelas no banco de dados
user.Base.metadata.create_all(bind=engine)
repertorio.Base.metadata.create_all(bind=engine)
agenda.Base.metadata.create_all(bind=engine)
recado.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para o portal do Setor Musical de Campo Grande/MS.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# As rotas e prefixos permanecem os mesmos
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/users", tags=["Usuários"])
app.include_router(repertorio_router.router, prefix="/repertorio", tags=["Repertório"])
app.include_router(agenda_router.router, prefix="/agenda", tags=["Agenda"])
app.include_router(recados_router.router, prefix="/recados", tags=["Recados"])


@app.get("/", tags=["Root"], summary="Verifica se a API está online")
def read_root():
    """Verifica o status da API."""
    return {"status": "ok", "message": "Bem-vindo à API do Setor Musical MS"}
