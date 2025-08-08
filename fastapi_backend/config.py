# fastapi_backend/app/config.py
# Versão 02 25/07/2025 10:40
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Gerencia as configurações da aplicação, lendo de variáveis de ambiente
    ou usando os valores padrão definidos aqui.
    """
    # Chave secreta para assinar os tokens JWT.
    SECRET_KEY: str = "uma-chave-secreta-forte-e-dificil-de-adivinhar"
    
    # Algoritmo de hashing para os tokens JWT.
    ALGORITHM: str = "HS256"
    
    # Tempo de expiração do token de acesso em minutos (padrão: 7 dias).
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # URL de conexão com o banco de dados.
    # Este valor será sobrescrito pela variável de ambiente no docker-compose.yml.
    DATABASE_URL: str = "sqlite:///./data/setormusical.db"

    # Lista de origens permitidas a fazer requisições para a API (CORS).
    CORS_ORIGINS: List[str] = ["*"]

# Instância única das configurações que será importada em toda a aplicação.
settings = Settings()
