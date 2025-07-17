# fastapi_backend/schemas/agenda.py
# Versão 24 17/07/2025 22:21
from pydantic import BaseModel
from typing import Optional
from datetime import date

class AgendaItemBase(BaseModel):
    """Schema base com os campos comuns de um item da agenda."""
    group: str
    date: date
    title: str
    description: str
    active: bool = True

class AgendaItemCreate(AgendaItemBase):
    """Schema para a criação de um novo item da agenda."""
    pass

class AgendaItemUpdate(BaseModel):
    """Schema para atualização de um item da agenda. Todos os campos são opcionais."""
    group: Optional[str] = None
    date: Optional[date] = None
    title: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None

class AgendaItem(AgendaItemBase):
    """Schema para retornar os dados de um item da agenda da API."""
    id: int

    class Config:
        # Permite que o Pydantic mapeie os dados diretamente de um
        # modelo SQLAlchemy para este schema.
        from_attributes = True
