# fastapi_backend/app/config.py
# Versão 47 17/07/2025 23:35
import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Define as configurações da aplicação, lendo de variáveis de ambiente ou de um ficheiro .env.
    """
    # --- Configurações de Segurança (JWT) ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "uma-chave-secreta-padrao-muito-dificil-de-adivinhar")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 dias

    # --- Configuração do Banco de Dados ---
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/setormusical.db")
    
    # --- Configuração de CORS ---
    # CORREÇÃO: Adicionamos a variável CORS_ORIGINS de volta.
    CORS_ORIGINS: List[str] = ["https://setormusicalms.art.br", "http://setormusicalms.art.br"]

    class Config:
        # Pede ao Pydantic para ler as variáveis de um ficheiro .env, se existir.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Cria uma instância única das configurações que será importada em toda a aplicação.
settings = Settings()
