# setormusicalms/backend/app/main.py
# Conteúdo Final para: backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import user, repertorio, agenda, recado  # Importa da nova localização
from .routers import auth, users, repertorio as repertorio_router, agenda as agenda_router, recados as recados_router

# Cria as tabelas da base de dados
user.Base.metadata.create_all(bind=engine)
repertorio.Base.metadata.create_all(bind=engine)
agenda.Base.metadata.create_all(bind=engine)
recado.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para gerenciamento do Setor Musical Mokiti Okada MS",
    version="1.0.0"
)

# Configura o CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os routers com os prefixos corretos
app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/users", tags=["Usuários"])
app.include_router(repertorio_router.router, prefix="/repertorio", tags=["Repertório"])
app.include_router(agenda_router.router, prefix="/agenda", tags=["Agenda"])
app.include_router(recados_router.router, prefix="/recados", tags=["Recados"])

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok", "message": "Bem-vindo à API do Setor Musical MS"}
