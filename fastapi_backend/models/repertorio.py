# fastapi_backend/models/repertorio.py
# Versão 01 25/07/2025 11:25
from sqlalchemy import Column, Integer, String, Boolean, JSON, Text
from database import Base

class RepertorioItem(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'repertorio_items' no banco de dados.
    """
    __tablename__ = "repertorio_items"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False, index=True)  # "Coral" ou "Orquestra"
    title = Column(String(200), nullable=False)
    arrangement = Column(String(200), nullable=True)
    year = Column(Integer, nullable=False)
    
    # URLs para mídias externas. O tipo Text permite URLs longas.
    audio_url = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True)
    video_thumbnail_url = Column(Text, nullable=True) # Armazena a thumbnail do vídeo
    sheet_music_url = Column(Text, nullable=False)
    
    # JSON é ideal para armazenar listas de strings de forma flexível.
    naipes = Column(JSON, default=list)  # Ex: ["Soprano", "Contralto"]
    grupos = Column(JSON, default=list)  # Ex: ["Grupo 1", "Novos"]
    
    active = Column(Boolean, default=True)
