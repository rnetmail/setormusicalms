# /fastapi_backend/app/routers/agenda.py
# v1.1 - 2025-07-30 02:15:19 - Corrige importações para o padrão absoluto do projeto.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Correção: Importações absolutas a partir da raiz do pacote 'app'
from app import schemas
from app.database import get_db
from app.crud import agenda as crud_agenda
from app.crud import user as crud_user

router = APIRouter()

@router.post("/", response_model=schemas.Agenda, status_code=status.HTTP_201_CREATED)
def create_agenda_item(
    item: schemas.AgendaCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Cria um novo item na agenda. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to create an agenda item")
    return crud_agenda.create_agenda_item(db=db, item=item)

@router.get("/", response_model=List[schemas.Agenda])
def read_agenda_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista de itens da agenda.
    """
    items = crud_agenda.get_agenda_items(db, skip=skip, limit=limit)
    return items

@router.get("/{item_id}", response_model=schemas.Agenda)
def read_agenda_item(item_id: int, db: Session = Depends(get_db)):
    """
    Retorna um item específico da agenda pelo ID.
    """
    db_item = crud_agenda.get_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Agenda item not found")
    return db_item

@router.put("/{item_id}", response_model=schemas.Agenda)
def update_agenda_item(
    item_id: int, 
    item: schemas.AgendaUpdate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Atualiza um item da agenda. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to update an agenda item")
    
    db_item = crud_agenda.get_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Agenda item not found")
        
    return crud_agenda.update_agenda_item(db=db, item_id=item_id, item_update=item)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agenda_item(
    item_id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Deleta um item da agenda. Requer autenticação de superusuário.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions to delete an agenda item")
        
    db_item = crud_agenda.get_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Agenda item not found")
        
    crud_agenda.delete_agenda_item(db=db, item_id=item_id)
    return {"ok": True}
