# fastapi_backend/app/config.py
# Versão 08 16/07/2025 21:15
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
    # CORREÇÃO: O valor padrão agora é o caminho para o banco de dados SQLite
    # dentro do volume do Docker, conforme definido no docker-compose.yml.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/setormusical.db")

    class Config:
        # Pede ao Pydantic para ler as variáveis de um ficheiro .env, se existir.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Cria uma instância única das configurações para ser usada em toda a aplicação.
settings = Settings()
