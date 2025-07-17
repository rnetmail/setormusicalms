# fastapi_backend/models/__init__.py
# Versão 76 18/07/2025 09:10

# Este ficheiro importa todos os modelos para que possam ser
# facilmente acedidos a partir do pacote 'models'.
from .user import User
from .repertorio import RepertorioItem
from .agenda import AgendaItem
from .recado import RecadoItem

__all__ = ["User", "RepertorioItem", "AgendaItem", "RecadoItem"]
