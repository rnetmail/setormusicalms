# fastapi_backend/schemas/recado.py
# Versão 50 17/07/2025 23:45
from pydantic import BaseModel
from typing import Optional
from datetime import date

class RecadoItemBase(BaseModel):
    """Schema base com os campos comuns de um item de recado."""
    group: str
    date: date
    title: str
    description: str
    active: bool = True

class RecadoItemCreate(RecadoItemBase):
    """Schema para a criação de um novo item de recado."""
    pass

class RecadoItemUpdate(BaseModel):
    """Schema para atualização de um item de recado. Todos os campos são opcionais."""
    group: Optional[str] = None
    date: Optional[date] = None
    title: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None

class RecadoItem(RecadoItemBase):
    """Schema para retornar os dados de um item de recado da API."""
    id: int

    class Config:
        # Permite que o Pydantic mapeie os dados diretamente de um
        # modelo SQLAlchemy para este schema.
        from_attributes = True
