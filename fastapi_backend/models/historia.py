# fastapi_backend/models/historia.py
# Versão 01 25/07/2025 13:50
from sqlalchemy import Column, Integer, String, Text
from database import Base

class HistoriaItem(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'historia_items' no banco de dados.
    """
    __tablename__ = "historia_items"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    imageUrl = Column(Text, nullable=True) # URL para a imagem do evento histórico
