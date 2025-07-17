# fastapi_backend/app/routers/recados.py
# Versão 12 17/07/2025 17:12
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

# Importações de módulos da aplicação
import crud.recado
import models.user
import schemas.recado
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user

router = APIRouter(prefix="/recados", tags=["Recados"])

@router.get("/", response_model=List[schemas.recado.RecadoItem])
def read_recado_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    group_filter: Optional[str] = Query(None, description="Filtrar por grupo: Coral, Orquestra, ou Setor"),
    # Qualquer usuário logado e ativo pode listar os recados.
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Lista os recados com filtros e paginação."""
    try:
        items = crud.recado.get_recado_items(db, skip=skip, limit=limit, group_filter=group_filter)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar recados: {e}")

@router.post("/", response_model=schemas.recado.RecadoItem, status_code=status.HTTP_201_CREATED)
def create_recado_item(
    item: schemas.recado.RecadoItemCreate,
    db: Session = Depends(get_db),
    # Apenas usuários com permissão de staff podem criar recados.
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Cria um novo recado."""
    try:
        return crud.recado.create_recado_item(db=db, item=item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar recado: {e}")

@router.get("/{item_id}", response_model=schemas.recado.RecadoItem)
def read_recado_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Obtém um recado específico pelo seu ID."""
    db_item = crud.recado.get_recado_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado não encontrado.")
    return db_item

@router.put("/{item_id}", response_model=schemas.recado.RecadoItem)
def update_recado_item(
    item_id: int,
    item_update: schemas.recado.RecadoItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Atualiza um recado."""
    db_item_check = crud.recado.get_recado_item(db, item_id=item_id)
    if db_item_check is None:
        raise HTTPException(status_code=404, detail="Recado não encontrado.")
    
    try:
        return crud.recado.update_recado_item(db, item_id=item_id, item_update=item_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar recado: {e}")

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recado_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Apaga um recado."""
    db_item = crud.recado.delete_recado_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Recado não encontrado para exclusão.")
    return None
