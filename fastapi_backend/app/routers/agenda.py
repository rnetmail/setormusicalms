# fastapi_backend/app/routers/agenda.py
# Versão 10 17/07/2025 17:08
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

# Importações de módulos da aplicação
import crud.agenda
import models.user
import schemas.agenda
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user

router = APIRouter(prefix="/agenda", tags=["Agenda"])

@router.get("/", response_model=List[schemas.agenda.AgendaItem])
def read_agenda_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None, description="Filtrar por grupo: Coral, Orquestra, ou Setor"),
    # Qualquer usuário logado e ativo pode listar os itens.
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Lista os itens da agenda com filtros e paginação."""
    try:
        items = crud.agenda.get_agenda_items(db, skip=skip, limit=limit, group_filter=group_filter)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar itens da agenda: {e}")

@router.post("/", response_model=schemas.agenda.AgendaItem, status_code=status.HTTP_201_CREATED)
def create_agenda_item(
    item: schemas.agenda.AgendaItemCreate,
    db: Session = Depends(get_db),
    # Apenas usuários com permissão de staff podem criar itens.
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Cria um novo item na agenda."""
    try:
        return crud.agenda.create_agenda_item(db=db, item=item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar item da agenda: {e}")

@router.get("/{item_id}", response_model=schemas.agenda.AgendaItem)
def read_agenda_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Obtém um item da agenda específico pelo seu ID."""
    db_item = crud.agenda.get_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da agenda não encontrado.")
    return db_item

@router.put("/{item_id}", response_model=schemas.agenda.AgendaItem)
def update_agenda_item(
    item_id: int,
    item_update: schemas.agenda.AgendaItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Atualiza um item da agenda."""
    db_item_check = crud.agenda.get_agenda_item(db, item_id=item_id)
    if db_item_check is None:
        raise HTTPException(status_code=404, detail="Item da agenda não encontrado.")

    try:
        return crud.agenda.update_agenda_item(db, item_id=item_id, item_update=item_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar item da agenda: {e}")

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agenda_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Apaga um item da agenda."""
    db_item = crud.agenda.delete_agenda_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item da agenda não encontrado para exclusão.")
    return None
