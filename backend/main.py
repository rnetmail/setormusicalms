# setormusicalms\backend\amain.py
from fastapi.middleware.cors import CORSMiddleware
from routers import auth
from database.database import engine, Base

# Cria todas as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

from pydantic import BaseModel
from typing import Optional, List

class RepertorioItemBase(BaseModel):

# setormusicalms\backend\security\security.py
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
import os

Converte links do Google Drive para links de visualização direta ou download.
"""
import re

def convert_google_drive_link(url: str, media_type: str = "view") -> str:
    """
