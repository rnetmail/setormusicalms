# fastapi_backend/schemas/galeria.py
# Versão 01 25/07/2025 13:58
from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import date

class GaleriaItemBase(BaseModel):
    """Schema base com os campos comuns de um item da galeria."""
    group: str
    title: str
    description: Optional[str] = None
    imageUrl: str  # Usamos str para aceitar URLs processadas/internas
    date: date

class GaleriaItemCreate(GaleriaItemBase):
    """Schema para a criação de um novo item da galeria."""
    pass

class GaleriaItemUpdate(BaseModel):
    """Schema para atualização de um item da galeria. Todos os campos são opcionais."""
    group: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    date: Optional[date] = None

class GaleriaItem(GaleriaItemBase):
    """Schema para retornar os dados de um item da galeria da API."""
    id: int

    class Config:
        from_attributes = True
