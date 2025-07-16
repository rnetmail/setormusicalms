# D:\backend\tests\conftest.py
# Versão 2 17/07/2024 16:45

import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.database import Base, get_db
from app.main import app

# Crie um engine de banco de dados em memória para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Crie uma sessão maker para interagir com o banco de dados
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Fixture que gerencia a sessão do banco de dados para os testes.

    - Cria todas as tabelas antes de cada teste.
    - Substitui a dependência `get_db` da aplicação para usar a sessão de teste.
    - Fornece a sessão de teste para ser usada nas verificações.
    - Limpa as tabelas e a substituição da dependência após o teste.
    """
    # Cria todas as tabelas no banco de dados em memória
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    def get_db_override() -> Generator[Session, None, None]:
        """Função que substitui a dependência get_db original."""
        yield db

    # Aplica a substituição da dependência na aplicação FastAPI
    app.dependency_overrides[get_db] = get_db_override

    try:
        # Fornece a sessão para o teste
        yield db
    finally:
        # Garante que tudo será limpo após o teste, mesmo em caso de erro
        db.close()
        # Remove todas as tabelas
        Base.metadata.drop_all(bind=engine)
        # Limpa a substituição da dependência para não afetar outros testes
        app.dependency_overrides.clear()