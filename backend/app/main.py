# setormusicalms/backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models

# Esta linha garante que o SQLAlchemy crie todas as tabelas
# definidas nos seus módulos de models quando a aplicação iniciar.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Setor Musical MS API",
    description="API para o sistema de gerenciamento do Setor Musical MS.",
    version="1.0.0"
)

# Configura o Cross-Origin Resource Sharing (CORS).
# É importante para permitir que seu frontend (rodando em outra porta/domínio)
# possa fazer requisições para esta API.
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    # Adicione aqui o domínio do seu frontend em produção.
    # Ex: "https://www.setormusicalms.com.br"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ponto de entrada raiz para verificar se a API está no ar.
@app.get("/")
async def read_root():
    """
    Endpoint raiz que retorna uma mensagem de boas-vindas.
    Útil para health checks simples.
    """
    return {"message": "Bem-vindo à API do Setor Musical MS"}

# Exemplo de como incluir rotas de outros arquivos para organizar o código.
# Descomente e ajuste conforme necessário.
# from .routers import users, items
#
# app.include_router(users.router, prefix="/api/v1", tags=["Users"])
# app.include_router(items.router, prefix="/api/v1", tags=["Items"])
