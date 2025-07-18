# fastapi_backend/app/routers/repertorio.py
# Versão 17 18/07/2025 00:05
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

# Importações absolutas, utilizando a nova estrutura de pacotes
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user
from crud import repertorio as crud_repertorio
from models import user as model_user
from schemas import repertorio as schema_repertorio

router = APIRouter(prefix="/repertorio", tags=["Repertório"])

@router.get("/", response_model=List[schema_repertorio.RepertorioItem])
def read_repertorio_items(
    skip: int = 0,
    limit: int = 100,
    type_filter: Optional[str] = Query(None, description="Filtrar por tipo: Coral ou Orquestra"),
    db: Session = Depends(get_db),
    # Acesso público ao repertório não requer autenticação neste modelo.
    # Se fosse privado, usaríamos 'Depends(get_current_active_user)'.
):
    """Lista os itens do repertório com filtros e paginação."""
    items = crud_repertorio.get_repertorio_items(db, skip=skip, limit=limit, type_filter=type_filter)
    return items

@router.post("/", response_model=schema_repertorio.RepertorioItem, status_code=status.HTTP_201_CREATED)
def create_repertorio_item(
    item: schema_repertorio.RepertorioItemCreate,
    db: Session = Depends(get_db),
    # Apenas usuários staff podem criar itens no repertório.
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Cria um novo item de repertório."""
    return crud_repertorio.create_repertorio_item(db=db, item=item)

@router.get("/{item_id}", response_model=schema_repertorio.RepertorioItem)
def read_repertorio_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Obtém um item de repertório específico pelo ID."""
    db_item = crud_repertorio.get_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item de repertório não encontrado.")
    return db_item

@router.put("/{item_id}", response_model=schema_repertorio.RepertorioItem)
def update_repertorio_item(
    item_id: int,
    item_update: schema_repertorio.RepertorioItemUpdate,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Atualiza um item de repertório."""
    db_item = crud_repertorio.update_repertorio_item(db, item_id=item_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item de repertório não encontrado para atualização.")
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repertorio_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_staff_user)
):
    """Apaga um item de repertório."""
    db_item = crud_repertorio.delete_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item de repertório não encontrado para exclusão.")
    return
