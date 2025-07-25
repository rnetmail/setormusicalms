# fastapi_backend/models/user.py
# Versão 01 25/07/2025 10:55
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..app.database import Base

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
    
    # Papéis e permissões
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)      # Permissão geral para gestão
    is_superuser = Column(Boolean, default=False) # Acesso total (Admin)
    
    # Timestamps automáticos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
