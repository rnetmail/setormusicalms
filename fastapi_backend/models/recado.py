# fastapi_backend/models/recado.py
# Versão 01 25/07/2025 13:45
from sqlalchemy import Column, Integer, String, Boolean, Date, Text
from database import Base

class RecadoItem(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'recado_items' no banco de dados.
    """
    __tablename__ = "recado_items"

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String(50), nullable=False, index=True)  # "Coral", "Orquestra", ou "Setor"
    date = Column(Date, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
