# fastapi_backend/schemas/__init__.py
# Versão 78 21/07/2025 11:03

from .user import User, UserCreate, UserUpdate, Token, TokenData
from .repertorio import RepertorioItem, RepertorioItemCreate, RepertorioItemUpdate
from .agenda import AgendaItem, AgendaItemCreate, AgendaItemUpdate
from .recado import RecadoItem, RecadoItemCreate, RecadoItemUpdate
from .historia import HistoriaItem, HistoriaItemCreate, HistoriaItemUpdate

# A linha __all__ define o que é exportado quando alguém faz 'from schemas import *'
__all__ = [
    "User", "UserCreate", "UserUpdate", "Token", "TokenData",
    "RepertorioItem", "RepertorioItemCreate", "RepertorioItemUpdate",
    "AgendaItem", "AgendaItemCreate", "AgendaItemUpdate",
    "RecadoItem", "RecadoItemCreate", "RecadoItemUpdate",
    "HistoriaItem", "HistoriaItemCreate", "HistoriaItemUpdate",
]
