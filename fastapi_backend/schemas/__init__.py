# fastapi_backend/schemas/__init__.py
# Versão 80 26/07/2025 11:05

from .user import User, UserCreate, UserUpdate
from .token import Token, TokenData  # <-- ADICIONAR ESTA LINHA
from .repertorio import RepertorioItem, RepertorioItemCreate, RepertorioItemUpdate
from .agenda import AgendaItem, AgendaItemCreate, AgendaItemUpdate
from .recado import RecadoItem, RecadoItemCreate, RecadoItemUpdate
from .historia import HistoriaItem, HistoriaItemCreate, HistoriaItemUpdate
from .galeria import GaleriaItem, GaleriaItemCreate, GaleriaItemUpdate

__all__ = [
    "User", "UserCreate", "UserUpdate", "Token", "TokenData", # <-- ADICIONAR TOKEN E TOKENDATA AQUI
    "RepertorioItem", "RepertorioItemCreate", "RepertorioItemUpdate",
    "AgendaItem", "AgendaItemCreate", "AgendaItemUpdate",
    "RecadoItem", "RecadoItemCreate", "RecadoItemUpdate",
    "HistoriaItem", "HistoriaItemCreate", "HistoriaItemUpdate",
    "GaleriaItem", "GaleriaItemCreate", "GaleriaItemUpdate",
]
