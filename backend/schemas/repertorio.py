# setormusicalms/backend/schemas/repertorio.py
from pydantic import BaseModel
from typing import Optional

# Schema base com os campos que são comuns para criação e leitura.
class RepertorioItemBase(BaseModel):
    """Campos base para um item do repertório."""
    title: str
    singer: Optional[str] = None
    year: Optional[str] = None
    lyrics: Optional[str] = None
    ciphers: Optional[str] = None
    tags: Optional[str] = None
    observations: Optional[str] = None
    type: str  # Ex: "Louvor", "Hino", "Corinho"
    active: bool = True

class RepertorioItemCreate(RepertorioItemBase):
    """
    Schema usado para criar um novo item no repertório.
    Herda todos os campos de RepertorioItemBase.
    """
    pass

class RepertorioItemUpdate(BaseModel):
    """
    Schema usado para atualizar um item existente.
    Todos os campos são opcionais para permitir atualizações parciais.
    """
    title: Optional[str] = None
    singer: Optional[str] = None
    year: Optional[str] = None
    lyrics: Optional[str] = None
    ciphers: Optional[str] = None
    tags: Optional[str] = None
    observations: Optional[str] = None
    type: Optional[str] = None
    active: Optional[bool] = None

class RepertorioItem(RepertorioItemBase):
    """
    Schema principal, usado para retornar dados da API.
    Inclui o 'id' e outros campos que são lidos do banco de dados.
    """
    id: int

    class Config:
        # Esta configuração permite que o Pydantic mapeie os dados
        # diretamente de um modelo SQLAlchemy para este schema.
        from_attributes = True
