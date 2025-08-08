# /fastapi_backend/app/routers/historia.py
# v2.1 - 2025-08-07 - Corrige importações para absolutas.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# --- INÍCIO DA CORREÇÃO ---
from schemas import historia as historia_schemas, user as user_schemas
from database import get_db
from crud import historia as crud_historia, user as crud_user
# --- FIM DA CORREÇÃO ---

router = APIRouter(prefix="/api/historia", tags=["Historia"])

@router.post("/", response_model=historia_schemas.HistoriaItem, status_code=status.HTTP_201_CREATED)
def create_historia_entry(
    historia: historia_schemas.HistoriaItemCreate, 
    db: Session = Depends(get_db), 
    current_user: user_schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Cria uma nova entrada na história. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud_historia.create_historia(db=db, historia=historia)

@router.get("/", response_model=List[historia_schemas.HistoriaItem])
def read_historias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna todas as entradas da história.
    """
    historias = crud_historia.get_historias(db, skip=skip, limit=limit)
    return historias

@router.get("/{historia_id}", response_model=historia_schemas.HistoriaItem)
def read_historia(historia_id: int, db: Session = Depends(get_db)):
    """
    Retorna uma entrada específica da história pelo ID.
    """
    db_historia = crud_historia.get_historia(db, historia_id=historia_id)
    if db_historia is None:
        raise HTTPException(status_code=404, detail="Historia entry not found")
    return db_historia

@router.put("/{historia_id}", response_model=historia_schemas.HistoriaItem)
def update_historia_entry(
    historia_id: int, 
    historia: historia_schemas.HistoriaItemUpdate, 
    db: Session = Depends(get_db), 
    current_user: user_schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Atualiza uma entrada da história. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_historia = crud_historia.get_historia(db, historia_id=historia_id)
    if db_historia is None:
        raise HTTPException(status_code=404, detail="Historia entry not found")
        
    return crud_historia.update_historia(db=db, historia_id=historia_id, historia_update=historia)

@router.delete("/{historia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_historia_entry(
    historia_id: int, 
    db: Session = Depends(get_db), 
    current_user: user_schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Deleta uma entrada da história. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    db_historia = crud_historia.get_historia(db, historia_id=historia_id)
    if db_historia is None:
        raise HTTPException(status_code=404, detail="Historia entry not found")
        
    crud_historia.delete_historia(db=db, historia_id=historia_id)
    return {"ok": True}
