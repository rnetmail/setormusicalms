# fastapi_backend/auth/hashing.py
# Versão 01 26/07/2025 12:55

from passlib.context import CryptContext

# Cria o contexto de hashing uma única vez
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto plano corresponde a uma senha hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha em texto plano."""
    return pwd_context.hash(password)
