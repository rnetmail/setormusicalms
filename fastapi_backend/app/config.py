# fastapi_backend/app/config.py
# Versão 01 25/07/2025 10:01
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Gerencia as configurações da aplicação, lendo de variáveis de ambiente.
    Centraliza todas as configurações em um único local.
    """
    # Chave secreta para assinar os tokens JWT. DEVE ser alterada em produção.
    SECRET_KEY: str = "asdfghjklqwertyuiopzxcvbnm,.;0192384576"
    
    # Algoritmo de hashing para os tokens JWT.
    ALGORITHM: str = "HS256"
    
    # Tempo de expiração do token de acesso em minutos (7 dias).
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # URL de conexão com o banco de dados SQLite.
    DATABASE_URL: str = "sqlite:///./data/setormusical.db"

    # Lista de origens permitidas a fazer requisições para a API (CORS).
    # Em produção, deve ser restrito ao domínio do frontend.
    CORS_ORIGINS: List[str] = ["*"] # Permite todos para desenvolvimento

    class Config:
        # Define o nome do arquivo .env a ser lido para carregar as variáveis.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instância única das configurações que será importada em toda a aplicação.
settings = Settings()
