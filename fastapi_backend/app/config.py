# fastapi_backend/app/config.py
# Versão 02 17/07/2025 23:35
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Define as configurações da aplicação, lendo de variáveis de ambiente ou
    de um ficheiro .env. Centraliza todas as configurações em um único local.
    """
    # --- Configurações de Segurança (JWT) ---
    # Chave secreta para assinar os tokens JWT. Deve ser um valor longo e aleatório.
    # É crucial que este valor seja mantido em segredo em produção.
    SECRET_KEY: str = "uma-chave-secreta-padrao-muito-dificil-de-adivinhar-em-desenvolvimento"
    
    # Algoritmo de hashing para os tokens JWT. HS256 é o padrão recomendado.
    ALGORITHM: str = "HS256"
    
    # Tempo de expiração do token de acesso em minutos.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    # --- Configuração do Banco de Dados ---
    # URL de conexão com o banco de dados. Para SQLite, o caminho para o arquivo.
    # Exemplo para PostgreSQL: "postgresql://user:password@host:port/dbname"
    DATABASE_URL: str = "sqlite:///./data/setormusical.db"
    
    # --- Configuração de CORS (Cross-Origin Resource Sharing) ---
    # Lista de origens permitidas a fazer requisições para a API.
    # Em produção, deve ser restrito ao domínio do frontend.
    # Ex: ["https://setormusicalms.art.br"]
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        # Define o nome do arquivo .env a ser lido para carregar as variáveis de ambiente.
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Cria uma instância única das configurações que será importada em toda a aplicação.
settings = Settings()
