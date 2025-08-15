# fastapi_backend/app/config.py
# Versão 03 - 12/08/2025 - Configurado para usar exclusivamente PostgreSQL
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

    # Configuração do PostgreSQL
    POSTGRES_DB: str = "setormusicalms_db"
    POSTGRES_USER: str = "mestre"
    POSTGRES_PASSWORD: str = "Setor@MS25"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    
    # URL de conexão com o banco de dados PostgreSQL.
    # Este valor será construído com os parâmetros de ambiente no docker-compose.yml.
    DATABASE_URL: str = "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

    # Lista de origens permitidas a fazer requisições para a API (CORS).
    CORS_ORIGINS: List[str] = ["*"]

# Instância única das configurações que será importada em toda a aplicação.
settings = Settings()