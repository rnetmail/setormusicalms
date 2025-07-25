# fastapi_backend/schemas/__init__.py
# Versão 02 25/07/2025 14:28
from .user import User, UserCreate, UserUpdate, Token, TokenData
from .repertorio import RepertorioItem, RepertorioItemCreate, RepertorioItemUpdate
from .agenda import AgendaItem, AgendaItemCreate, AgendaItemUpdate
from .recado import RecadoItem, RecadoItemCreate, RecadoItemUpdate
from .historia import HistoriaItem, HistoriaItemCreate, HistoriaItemUpdate
from .galeria import GaleriaItem, GaleriaItemCreate, GaleriaItemUpdate

# A lista __all__ define o que é exportado quando se utiliza "from schemas import *"
__all__ = [
    "User", "UserCreate", "UserUpdate", "Token", "TokenData",
    "RepertorioItem", "RepertorioItemCreate", "RepertorioItemUpdate",
    "AgendaItem", "AgendaItemCreate", "AgendaItemUpdate",
    "RecadoItem", "RecadoItemCreate", "RecadoItemUpdate",
    "HistoriaItem", "HistoriaItemCreate", "HistoriaItemUpdate",
    "GaleriaItem", "GaleriaItemCreate", "GaleriaItemUpdate",
]
