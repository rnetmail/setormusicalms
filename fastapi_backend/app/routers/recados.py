# fastapi_backend/app/routers/recados.py
# Versão 16 18/07/2025 00:04
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

# Importações absolutas, utilizando a nova estrutura de pacotes
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user
from crud import recado as crud_recado
from models import user as model_user
from schemas import recado as schema_recado

router = APIRouter(prefix="/recados", tags=["Recados"])

@router.get("/", response_model=List[schema_recado.RecadoItem])
def read_recado_items(
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None, description="Filtrar por grupo: Coral, Orquestra, ou Setor"),
    db: Session = Depends(get_db),
    # Qualquer usuário logado pode visualizar os recados.
    current_user: model_user.User = Depends(get_current_active_user)
):
    """Lista os recados com filtros e paginação."""
    items = crud_recado.get_recado_items(db, skip=skip, limit=limit, group_filter=group_filter)
    return items

@router.post("/", response_model=schema_recado.RecadoItem, status_code=status.HTTP_201_CREATED)
def create_recado_item(
    item: schema_recado.RecadoItemCreate,
    db: Session = Depends(get_db),
    # Apenas usuários staff podem criar recados.
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Cria um novo recado."""
    return crud_recado.create_recado_item(db=db, item=item)

@router.get("/{item_id}", response_model=schema_recado.RecadoItem)
def read_recado_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_active_user)
):
    """Obtém um recado específico pelo ID."""
    db_item = crud_recado.get_recado_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado não encontrado.")
    return db_item

@router.put("/{item_id}", response_model=schema_recado.RecadoItem)
def update_recado_item(
    item_id: int,
    item_update: schema_recado.RecadoItemUpdate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Atualiza um recado."""
    db_item = crud_recado.update_recado_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado não encontrado para atualização.")
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recado_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Apaga um recado."""
    db_item = crud_recado.delete_recado_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado não encontrado para exclusão.")
    return
