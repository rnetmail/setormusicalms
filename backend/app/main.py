# fastapi_backend/app/main.py
# Versão 01 16/07/2025 20:20
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import user, repertorio, agenda, recado
from .routers import auth, users, repertorio as repertorio_router, agenda as agenda_router, recados as recados_router

# Cria as tabelas da base de dados se não existirem
user.Base.metadata.create_all(bind=engine)
repertorio.Base.metadata.create_all(bind=engine)
agenda.Base.metadata.create_all(bind=engine)
recado.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para gerenciamento do Setor Musical Mokiti Okada MS",
    version="1.0.0"
)

# Configura o CORS para permitir requisições de qualquer origem,
# o que é essencial para o ambiente de desenvolvimento e produção com domínios diferentes.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Agrupa todas as rotas sob um prefixo /api principal
api_router = APIRouter(prefix="/api")

# Inclui os routers de cada módulo
api_router.include_router(auth.router, tags=["Autenticação"])
api_router.include_router(users.router, tags=["Usuários"])
api_router.include_router(repertorio_router.router, tags=["Repertório"])
api_router.include_router(agenda_router.router, tags=["Agenda"])
api_router.include_router(recados_router.router, tags=["Recados"])

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raiz para verificar se a API está no ar."""
    return {"status": "ok", "message": "Bem-vindo à API do Setor Musical MS"}

@app.get("/api/health", tags=["Health Check"])
def health_check():
    """Endpoint de verificação de saúde para monitoramento."""
    return {"status": "healthy", "message": "API está funcionando corretamente"}
