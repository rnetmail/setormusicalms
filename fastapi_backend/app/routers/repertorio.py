# fastapi_backend/app/routers/repertorio.py
# Versão 20 - Endpoint Protegido

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from schemas import repertorio as schema_repertorio
from crud import repertorio as crud_repertorio
from models import user as model_user
from auth.security import get_current_active_user, get_current_staff_user

router = APIRouter(prefix="/repertorio", tags=["Repertório"])

@router.get("/", response_model=List[schema_repertorio.RepertorioItem])
def read_repertorio_items(
    skip: int = 0,
    limit: int = 100,
    type_filter: Optional[str] = Query(None, description="Filtrar por tipo: Coral ou Orquestra"),
    db: Session = Depends(get_db),
    # CORREÇÃO DE SEGURANÇA: Endpoint agora protegido, requer usuário autenticado.
    current_user: model_user.User = Depends(get_current_active_user)
):
    """Lista os itens do repertório com filtros e paginação. Requer autenticação."""
    items = crud_repertorio.get_repertorio_items(db, skip=skip, limit=limit, type_filter=type_filter)
    return items

# O restante do arquivo (POST, PUT, DELETE, etc.) permanece o mesmo.
# Adicione a dependência `Depends(get_current_active_user)` aos outros endpoints GET se necessário.
@router.get("/{item_id}", response_model=schema_repertorio.RepertorioItem)
def read_repertorio_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: model_user.User = Depends(get_current_active_user)
):
    """Obtém um item de repertório específico pelo ID. Requer autenticação."""
    db_item = crud_repertorio.get_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item de repertório não encontrado.")
    return db_item
