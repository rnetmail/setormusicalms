# fastapi_backend/models/agenda.py
# Versão 01 25/07/2025 11:38
from sqlalchemy import Column, Integer, String, Boolean, Date, Text
from database import Base

class AgendaItem(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'agenda_items' no banco de dados.
    """
    __tablename__ = "agenda_items"

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String(50), nullable=False, index=True)  # "Coral", "Orquestra", ou "Setor"
    date = Column(Date, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
