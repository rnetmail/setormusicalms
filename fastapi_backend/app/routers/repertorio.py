# /fastapi_backend/app/routers/repertorio.py
# v2.1 - 2025-08-07 - Corrige importações para absolutas.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# --- INÍCIO DA CORREÇÃO ---
# Importações absolutas a partir da raiz do projeto 'app'
from app.schemas import repertorio as repertorio_schemas, user as user_schemas
from app.database import get_db
from app.crud import repertorio as crud_repertorio, user as crud_user
# --- FIM DA CORREÇÃO ---

router = APIRouter(prefix="/api/repertorio", tags=["Repertorio"])

@router.post("/", response_model=repertorio_schemas.RepertorioItem, status_code=status.HTTP_201_CREATED)
def create_repertorio_item(
    item: repertorio_schemas.RepertorioItemCreate, 
    db: Session = Depends(get_db), 
    current_user: user_schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Cria uma nova música no repertório. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud_repertorio.create_repertorio_item(db=db, item=item)

@router.get("/", response_model=List[repertorio_schemas.RepertorioItem])
def read_repertorio_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna la lista de músicas do repertório.
