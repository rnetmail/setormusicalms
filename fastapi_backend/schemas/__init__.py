# fastapi_backend/schemas/__init__.py
# Versão 01 25/07/2025 11:05
from .user import User, UserCreate, UserUpdate, Token, TokenData

# A lista __all__ define quais nomes são exportados publicamente pelo pacote.
__all__ = [
    "User",
    "UserCreate",
    "UserUpdate",
    "Token",
    "TokenData",
]
