# fastapi_backend/models/__init__.py
# Versão 77 21/07/2025 11:02

# Este ficheiro importa todos os modelos para que possam ser
# facilmente acedidos a partir do pacote 'models'.
from .user import User
from .repertorio import RepertorioItem
from .agenda import AgendaItem
from .recado import RecadoItem
from .historia import HistoriaItem

__all__ = ["User", "RepertorioItem", "AgendaItem", "RecadoItem", "HistoriaItem"]
