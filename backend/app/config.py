# setormusicalms/backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configurações da aplicação.

    Estes valores são carregados a partir de variáveis de ambiente ou de um
    arquivo .env. É uma boa prática para gerenciar configurações de
    forma segura e flexível.
    """
    API_V1_STR: str = "/api/v1"

    # Exemplo de outras configurações que podem ser adicionadas:
    # SECRET_KEY: str = "sua_chave_secreta_super_segura"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        # Especifica que as configurações podem ser lidas de um arquivo .env
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Instância única das configurações que será usada em toda a aplicação
settings = Settings()
