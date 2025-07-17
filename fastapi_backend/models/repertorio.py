# fastapi_backend/models/repertorio.py
# Versão 18 16/07/2025 22:11
from sqlalchemy import Column, Integer, String, Boolean, JSON, Text
from app.database import Base

class RepertorioItem(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'repertorio_items' no banco de dados.
    """
    __tablename__ = "repertorio_items"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)  # Ex: 'Coral', 'Orquestra'
    title = Column(String(200), nullable=False)
    arrangement = Column(String(200), nullable=True)
    year = Column(Integer, nullable=False)
    
    # Usamos o tipo Text para permitir URLs longas.
    audio_url = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True)
    sheet_music_url = Column(Text, nullable=False)
    
    # O tipo JSON é ideal para armazenar listas de strings, como naipes ou grupos.
    naipes = Column(JSON, default=list)  # Para o Coral
    grupos = Column(JSON, default=list)  # Para a Orquestra
    
    active = Column(Boolean, default=True)
