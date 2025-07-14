from sqlalchemy import Column, Integer, String, Boolean, Date, Text
from app.database import Base

class RecadoItem(Base):
    __tablename__ = "recado_items"

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String(20), nullable=False)  # Coral, Orquestra, Setor
    date = Column(Date, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
