# setormusicalms/backend/app/config_local.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Configurações para o ambiente de desenvolvimento local.
    Pode ser usado para sobrescrever configurações de produção
    sem a necessidade de um arquivo .env.
    """
    API_V1_STR: str = "/api/v1"
