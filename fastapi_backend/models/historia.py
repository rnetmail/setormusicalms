# fastapi_backend/schemas/historia.py
# Versão 01 21/07/2025 10:50
from pydantic import BaseModel, HttpUrl
from typing import Optional

class HistoriaItemBase(BaseModel):
    """Schema base com os campos comuns de um item da história."""
    year: int
    title: str
    description: str
    imageUrl: Optional[HttpUrl] = None

class HistoriaItemCreate(HistoriaItemBase):
    """Schema para a criação de um novo item da história."""
    pass

class HistoriaItemUpdate(BaseModel):
    """Schema para atualização de um item da história. Todos os campos são opcionais."""
    year: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    imageUrl: Optional[HttpUrl] = None

class HistoriaItem(HistoriaItemBase):
    """Schema para retornar os dados de um item da história da API."""
    id: int

    class Config:
        # Permite que o Pydantic mapeie os dados diretamente de um
        # modelo SQLAlchemy para este schema.
        from_attributes = True
