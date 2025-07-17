# fastapi_backend/app/config.py
# Versão 01 17/07/2025 16:36
from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    """
    Define as configurações da aplicação, lendo de variáveis de ambiente ou de um ficheiro .env.
    A ordem de prioridade é: Variáveis de ambiente > .env file > valores padrão no código.
    """
    # --- Configurações de Segurança (JWT) ---
    SECRET_KEY: str = "uma-chave-secreta-padrao-muito-dificil-de-adivinhar-em-desenvolvimento"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    # --- Configuração do Banco de Dados ---
    # Para produção, use uma URL do PostgreSQL, ex:
    # DATABASE_URL=postgresql://user:password@host:port/dbname
    DATABASE_URL: str = "sqlite:///./data/setormusical.db"

    # --- Configuração de CORS (Cross-Origin Resource Sharing) ---
    # Lista de domínios autorizados a fazer requisições para a API.
    # Em produção, deve ser a URL exata do frontend.
    CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "https://setormusicalms.art.br"
    ]

    # --- Configuração do Admin Padrão ---
    # Credenciais para o superusuário a ser criado pelo script de inicialização.
    # Em produção, é altamente recomendável usar variáveis de ambiente para estes valores.
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "Setor@MS25"
    ADMIN_EMAIL: str = "admin@setormusicalms.art.br"

    class Config:
        # Pede ao Pydantic para ler as variáveis de um ficheiro .env, se existir.
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # Torna a classe compatível com a sintaxe de casos de uso (case-insensitive)
        case_sensitive = True

# Cria uma instância única das configurações que será importada em toda a aplicação.
settings = Settings()
