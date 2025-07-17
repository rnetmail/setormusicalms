# fastapi_backend/app/routers/repertorio.py
# Versão 08 17/07/2025 17:02
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

# Importações de módulos da aplicação
import crud.repertorio
import models.user
import schemas.repertorio
from app.database import get_db
from auth.security import get_current_staff_user, get_current_active_user

router = APIRouter(prefix="/repertorio", tags=["Repertório"])

@router.get("/", response_model=List[schemas.repertorio.RepertorioItem])
def read_repertorio_items(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    type_filter: Optional[str] = Query(None, description="Filtrar por tipo: Coral ou Orquestra"),
    # Qualquer usuário logado e ativo pode listar os itens.
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Lista os itens do repertório com filtros e paginação."""
    try:
        items = crud.repertorio.get_repertorio_items(db, skip=skip, limit=limit, type_filter=type_filter)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar itens do repertório: {e}")

@router.post("/", response_model=schemas.repertorio.RepertorioItem, status_code=status.HTTP_201_CREATED)
def create_repertorio_item(
    item: schemas.repertorio.RepertorioItemCreate,
    db: Session = Depends(get_db),
    # Apenas usuários com permissão de staff podem criar itens.
    current_user: models.user.User = Depends(get_current_staff_user)
):
    """Cria um novo item de repertório."""
    try:
        return crud.repertorio.create_repertorio_item(db=db, item=item)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar item de repertório: {e}")

@router.get("/{item_id}", response_model=schemas.repertorio.RepertorioItem)
def read_repertorio_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_active_user)
):
    """Obtém um item de repertório específico pelo seu ID."""
    db_item = crud.repertorio.get_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item de repertório não encontrado.")
    return db_item

@router.put("/{
