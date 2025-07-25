# fastapi_backend/models/__init__.py
# Versão 01 25/07/2025 10:57
# Este arquivo transforma o diretório 'models' em um pacote Python
# e define a sua interface pública.

from .user import User

# A lista __all__ define quais nomes são exportados quando se utiliza "from models import *"
__all__ = [
    "User" 
]
