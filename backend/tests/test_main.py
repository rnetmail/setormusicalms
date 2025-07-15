# backend/tests/test_main.py
import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# --- Configuração do Banco de Dados de Teste ---
# Usamos um banco de dados SQLite em memória para os testes.
# connect_args e StaticPool são necessários para o SQLite em um ambiente multi-thread.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas no banco de dados em memória antes de rodar os testes.
Base.metadata.create_all(bind=engine)

# --- Sobrescrita da Dependência (Dependency Override) ---
# Esta função será usada para substituir a dependência get_db original.
def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()

# Aplica a sobrescrita: toda vez que a aplicação pedir a dependência get_db,
# ela receberá a nossa versão de teste (override_get_db).
app.dependency_overrides[get_db] = override_get_db

# --- Testes da API ---
@pytest.mark.anyio
async def test_read_root():
    """
    Testa o endpoint raiz ("/") para garantir que ele retorna a mensagem esperada.
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API do Setor Musical MS está no ar."}
