# setormusicalms/backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importando os módulos de banco de dados e modelos
from database.database import engine, Base
# A importação 'models.user' foi removida, pois não era utilizada diretamente.
# Os modelos são carregados indiretamente através da importação do 'main_router'.

# Importando o roteador principal da aplicação
from app.main_production import router as main_router

# Este comando cria as tabelas no banco de dados com base nos seus modelos
# SQLAlchemy, caso elas ainda não existam.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para o sistema do Setor Musical MS",
    version="1.0.0"
)

# Configura o Cross-Origin Resource Sharing (CORS) para permitir
# que o frontend acesse a API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para produção, restrinja a origens específicas.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui todas as rotas definidas no arquivo main_production.py na aplicação principal.
app.include_router(main_router)

@app.get("/")
def read_root():
    """Endpoint raiz para verificar se a API está funcionando."""
    return {"message": "API do Setor Musical MS está no ar."}
