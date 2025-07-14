from pydantic import BaseModel
from typing import Optional
from datetime import date

class AgendaItemBase(BaseModel):
    group: str  # Coral, Orquestra, Setor
    date: date
    title: str
    description: str
    active: bool = True

class AgendaItemCreate(AgendaItemBase):
    pass

class AgendaItemUpdate(BaseModel):
    group: Optional[str] = None
    date: Optional[date] = None
    title: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None

class AgendaItem(AgendaItemBase):
    id: int

    class Config:
        from_attributes = True
