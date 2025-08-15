# fastapi_backend/auth/password.py
# Versão 01 25/07/2025 11:08
from passlib.context import CryptContext

# Cria um contexto para o hashing de senhas, especificando o algoritmo bcrypt.
# Esta é a prática recomendada para o armazenamento seguro de senhas.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde à sua versão hasheada.

    Args:
        plain_password: A senha fornecida pelo usuário (texto plano).
        hashed_password: A senha hasheada armazenada no banco de dados.

    Returns:
        True se as senhas corresponderem, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto plano.

    Args:
        password: A senha em texto plano a ser hasheada.

    Returns:
        A representação hasheada da senha.
    """
    return pwd_context.hash(password)
