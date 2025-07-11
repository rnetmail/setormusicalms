from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database_local import engine
from models.user_local import User
from app.routers import auth
from app.routers.repertorio_fixed import router as repertorio_router

# Criar tabelas
User.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API - Corrigida",
    description="API corrigida para gerenciamento do Setor Musical Mokiti Okada MS",
    version="1.0.1"
)

# Configurar CORS mais permissivo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas as origens
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Métodos específicos
    allow_headers=["*"],  # Permitir todos os headers
    expose_headers=["*"]  # Expor todos os headers
)

# Incluir routers
app.include_router(auth.router, prefix="/api")
app.include_router(repertorio_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "message": "Setor Musical MS API - Versão Corrigida", 
        "version": "1.0.1",
        "features": [
            "Filtros por grupo (Coral/Orquestra/Setor)",
            "Conversão automática de links do Google Drive",
            "Conversão automática de links do YouTube",
            "CORS configurado corretamente"
        ]
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy", 
        "message": "API corrigida funcionando",
        "cors": "enabled",
        "media_conversion": "enabled"
    }

@app.options("/{path:path}")
def options_handler(path: str):
    """Handler para requisições OPTIONS (CORS preflight)"""
    return {"message": "OK"}

# Middleware para debug de CORS
@app.middleware("http")
async def cors_debug_middleware(request, call_next):
    """Middleware para debug de CORS"""
    response = await call_next(request)
    
    # Adicionar headers CORS manualmente se necessário
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    
    return response
