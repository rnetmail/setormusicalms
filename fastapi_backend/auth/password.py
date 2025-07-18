# fastapi_backend/auth/password.py
# Versão 01 17/07/2025 23:30
from passlib.context import CryptContext

# Cria um contexto para o hashing de senhas, especificando o algoritmo bcrypt.
# O bcrypt é o padrão de mercado para armazenamento seguro de senhas.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde à sua versão hasheada.

    :param plain_password: A senha fornecida pelo usuário.
    :param hashed_password: A senha armazenada no banco de dados.
    :return: True se as senhas corresponderem, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto plano usando bcrypt.

    :param password: A senha a ser hasheada.
    :return: O hash da senha.
    """
    return pwd_context.hash(password)
