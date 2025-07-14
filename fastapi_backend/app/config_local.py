from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "sua-chave-secreta-super-forte-aqui-local"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    cors_origins: List[str] = ["https://setormusicalms.art.br", "http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"

settings = Settings()
