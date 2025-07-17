# fastapi_backend/models/agenda.py
# Versão 23 17/07/2025 22:19
from sqlalchemy import Column, Integer, String, Boolean, Date, Text
from app.database import Base

class AgendaItem(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'agenda_items' no banco de dados.
    """
    __tablename__ = "agenda_items"

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String(20), nullable=False)  # Ex: 'Coral', 'Orquestra', 'Setor'
    date = Column(Date, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
