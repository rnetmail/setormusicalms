# /fastapi_backend/app/routers/repertorio.py
# v1.1 - 2025-07-30 02:18:00 - Corrige importações para o padrão absoluto do projeto.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Correção: Importações absolutas a partir da raiz do pacote 'app'
from app import schemas
from app.database import get_db
from app.crud import repertorio as crud_repertorio
from app.crud import user as crud_user

router = APIRouter()

@router.post("/", response_model=schemas.Repertorio, status_code=status.HTTP_201_CREATED)
def create_repertorio_item(
    item: schemas.RepertorioCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Cria uma nova música no repertório. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud_repertorio.create_repertorio_item(db=db, item=item)

@router.get("/", response_model=List[schemas.Repertorio])
def read_repertorio_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna la lista de músicas do repertório.
    """
    items = crud_repertorio.get_repertorio_items(db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=schemas.Repertorio)
def read_repertorio_item(item_id: int, db: Session = Depends(get_db)):
    """
    Retorna uma música específica do repertório pelo ID.
    """
    db_item = crud_repertorio.get_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Repertorio item not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.Repertorio)
def update_repertorio_item(
    item_id: int, 
    item: schemas.RepertorioUpdate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Atualiza uma música do repertório. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    db_item = crud_repertorio.get_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Repertorio item not found")
        
    return crud_repertorio.update_repertorio_item(db=db, item_id=item_id, item_update=item)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repertorio_item(
    item_id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Deleta uma música do repertório. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    db_item = crud_repertorio.get_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Repertorio item not found")
        
    crud_repertorio.delete_repertorio_item(db=db, item_id=item_id)
    return {"ok": True}
