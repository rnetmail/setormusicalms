# Conteúdo corrigido para backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define o caminho para o ficheiro do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./setormusical.db"

# Cria a engine do SQLAlchemy
# O argumento 'connect_args' é necessário para o SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
