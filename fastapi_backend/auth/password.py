# fastapi_backend/auth/password.py
# Versão 04 17/07/2025 16:40
from passlib.context import CryptContext

# Define o contexto de criptografia, especificando o algoritmo 'bcrypt' como padrão.
# 'deprecated="auto"' instrui o passlib a atualizar automaticamente os hashes se
# um esquema mais novo for adicionado no futuro.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde à sua versão hasheada.

    Args:
        plain_password: A senha a ser verificada.
        hashed_password: O hash da senha armazenado no banco de dados.

    Returns:
        True se as senhas correspondem, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto plano usando o contexto definido.

    Args:
        password: A senha a ser hasheada.

    Returns:
        O hash da senha.
    """
    return pwd_context.hash(password)
