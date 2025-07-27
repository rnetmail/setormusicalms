# fastapi_backend/models/user.py
# Versão 02 25/07/2025 17:55
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
# CORREÇÃO: A importação agora é absoluta a partir da raiz do projeto.
from app.database import Base

class User(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'users' no banco de dados.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    full_name = Column(String(100), nullable=True)
    
    # Papéis e permissões
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Timestamps automáticos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
