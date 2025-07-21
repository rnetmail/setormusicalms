# fastapi_backend/models/galeria.py
# Versão 01 21/07/2025 14:11
from sqlalchemy import Column, Integer, String, Date, Text
from app.database import Base

class GaleriaItem(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'galeria_items' no banco de dados.
    Armazena imagens e vídeos da galeria.
    """
    __tablename__ = "galeria_items"

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String(20), nullable=False) # Ex: 'Coral', 'Orquestra'
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    imageUrl = Column(String(2048), nullable=False)
    date = Column(Date, nullable=False)
