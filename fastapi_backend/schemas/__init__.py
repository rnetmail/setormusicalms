# fastapi_backend/schemas/__init__.py
# Versão 79 21/07/2025 18:17

from .user import User, UserCreate, UserUpdate, Token, TokenData
from .repertorio import RepertorioItem, RepertorioItemCreate, RepertorioItemUpdate
from .agenda import AgendaItem, AgendaItemCreate, AgendaItemUpdate
from .recado import RecadoItem, RecadoItemCreate, RecadoItemUpdate
from .historia import HistoriaItem, HistoriaItemCreate, HistoriaItemUpdate
from .galeria import GaleriaItem, GaleriaItemCreate, GaleriaItemUpdate

# A linha __all__ define o que é exportado quando alguém faz 'from schemas import *'
__all__ = [
    "User", "UserCreate", "UserUpdate", "Token", "TokenData",
    "RepertorioItem", "RepertorioItemCreate", "RepertorioItemUpdate",
    "AgendaItem", "AgendaItemCreate", "AgendaItemUpdate",
    "RecadoItem", "RecadoItemCreate", "RecadoItemUpdate",
    "HistoriaItem", "HistoriaItemCreate", "HistoriaItemUpdate",
    "GaleriaItem", "GaleriaItemCreate", "GaleriaItemUpdate",
]
