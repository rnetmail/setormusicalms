from sqlalchemy import Column, Integer, String, Boolean, JSON, Text
from app.database import Base

class RepertorioItem(Base):
    __tablename__ = "repertorio_items"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)  # Coral, Orquestra, Setor
    title = Column(String(200), nullable=False)
    arrangement = Column(String(200), nullable=True)
    year = Column(Integer, nullable=False)
    audio_url = Column(Text, nullable=True)
    video_url = Column(Text, nullable=True)
    sheet_music_url = Column(Text, nullable=False)
    naipes = Column(JSON, default=list)
    grupos = Column(JSON, default=list)
    active = Column(Boolean, default=True)
