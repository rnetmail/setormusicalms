# fastapi_backend/crud/__init__.py
# Versão 01 25/07/2025 11:22
# Este arquivo transforma o diretório 'crud' em um pacote Python
# e define a sua interface pública.

from .user import (
    get_user,
    get_user_by_username,
    get_user_by_email,
    get_users,
    create_user,
    update_user,
    delete_user,
    authenticate_user,
)

# A lista __all__ define quais nomes são exportados quando se utiliza "from crud import *"
__all__ = [
    "get_user",
    "get_user_by_username",
    "get_user_by_email",
    "get_users",
    "create_user",
    "update_user",
    "delete_user",
    "authenticate_user",
]
