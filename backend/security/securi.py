# setormusicalms/backend/security/securi.py
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
import os

# --- Configuração de Segurança ---
# É altamente recomendável carregar estes valores de variáveis de ambiente.
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-padrao-muito-segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Cria um contexto para hashing de senhas.
# "bcrypt" é o algoritmo de hashing recomendado.
# O "deprecated="auto"" garante que hashes antigos possam ser atualizados.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Funções de Senha ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde a uma senha hasheada.

    Retorna True se as senhas corresponderem, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera o hash de uma senha em texto plano.

    Nunca armazene senhas em texto plano no banco de dados.
    """
    return pwd_context.hash(password)

# --- Funções de Token JWT ---

def create_access_token(data: dict) -> str:
    """
    Cria um novo token de acesso (JWT).

    O token contém os dados fornecidos (payload) e uma data de expiração.
    Ele é assinado com a SECRET_KEY para garantir sua autenticidade.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
