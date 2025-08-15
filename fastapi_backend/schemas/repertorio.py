# fastapi_backend/schemas/repertorio.py
# Versão 01 25/07/2025 11:28
from pydantic import BaseModel, Field
from typing import Optional, List

class RepertorioItemBase(BaseModel):
    """Schema base com os campos comuns de um item de repertório."""
    type: str
    title: str
    arrangement: Optional[str] = None
    year: int
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    sheet_music_url: str
    naipes: Optional[List[str]] = Field(default_factory=list)
    grupos: Optional[List[str]] = Field(default_factory=list)
    active: bool = True

class RepertorioItemCreate(RepertorioItemBase):
    """Schema usado para criar um novo item de repertório."""
    pass

class RepertorioItemUpdate(BaseModel):
    """
    Schema usado para atualizar um item de repertório.
    Todos os campos são opcionais para permitir atualizações parciais.
    """
    type: Optional[str] = None
    title: Optional[str] = None
    arrangement: Optional[str] = None
    year: Optional[int] = None
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    sheet_music_url: Optional[str] = None
    naipes: Optional[List[str]] = None
    grupos: Optional[List[str]] = None
    active: Optional[bool] = None

class RepertorioItem(RepertorioItemBase):
    """Schema usado para retornar os dados de um item de repertório da API."""
    id: int
    video_thumbnail_url: Optional[str] = None # Campo gerado pelo backend

    class Config:
        # Permite que o Pydantic mapeie os dados diretamente de um modelo SQLAlchemy.
        from_attributes = True
