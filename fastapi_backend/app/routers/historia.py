# fastapi_backend/app/routers/historia.py
# Versão 01 21/07/2025 10:55
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from auth.security import get_current_staff_user
from crud import historia as crud_historia
from models import user as model_user
from schemas import historia as schema_historia

router = APIRouter(prefix="/historia", tags=["História"])

@router.get("/", response_model=List[schema_historia.HistoriaItem])
def read_historia_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos os itens da história. Acesso público."""
    items = crud_historia.get_historia_items(db, skip=skip, limit=limit)
    return items

@router.post("/", response_model=schema_historia.HistoriaItem, status_code=status.HTTP_201_CREATED)
def create_historia_item(
    item: schema_historia.HistoriaItemCreate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
