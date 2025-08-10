# /fastapi_backend/database.py
# v2.0 - 2025-08-10 21:35:00 - Corrige importações e remove referências à pasta 'app'

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Correção: Importação direta do config
from config import settings

# Garante que o diretório para o arquivo do banco de dados exista.
# Extrai o caminho do arquivo da URL de conexão.
database_url = settings.DATABASE_URL
if database_url.startswith("sqlite"):
        db_path = database_url.split("///")[1]
        db_dir = os.path.dirname(db_path)
        if db_dir:
                    os.makedirs(db_dir, exist_ok=True)

    # Cria a engine do SQLAlchemy com a URL do banco de dados.
    # O argumento `connect_args` é específico para SQLite e permite que o banco de dados
    # seja acessado por múltiplas threads, o que é necessário para o FastAPI.
    engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False}
    )

# Cria uma classe SessionLocal que será usada para criar sessões do banco de dados.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base que será herdada por todos os nossos modelos ORM (tabelas).
Base = declarative_base()

def get_db():
        """
            Função de dependência do FastAPI para obter uma sessão do banco de dados por requisição.
                Garante que a sessão seja sempre fechada após o uso.
                    """
        db = SessionLocal()
        try:
                    yield db
finally:
        db.close()
