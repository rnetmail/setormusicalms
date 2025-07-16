# setormusicalms/backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Declaração das variáveis que serão lidas do ficheiro .env

    # Configuração do Banco de Dados SQLite (não lido do .env, mas definido no código)
    # Por isso, não precisamos declará-lo aqui.

    # Configurações de Segurança JWT
    SECRET_KEY: "Setor@MS25"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Informações do Admin para o script de inicialização
    ADMIN_USER: "setormusicalms"
    ADMIN_PASSWORD: "Setor@MS25"
    ADMIN_EMAIL: "rnetmail@gmail.com"

    class Config:
        # Aponta para o ficheiro .env que contém as variáveis
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Cria uma instância das configurações para ser usada em toda a aplicação
settings = Settings()
