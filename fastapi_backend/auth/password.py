# fastapi_backend/auth/password.py
# Versão 85 18/07/2025 10:05

from passlib.context import CryptContext

# Cria um contexto para o hashing de senhas, especificando o algoritmo bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde à sua versão hasheada.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto plano.
    """
    return pwd_context.hash(password)
