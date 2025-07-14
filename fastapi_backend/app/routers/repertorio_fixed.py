from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database_local import get_db
from auth.security import get_current_active_user
from crud.repertorio_fixed import (
    get_repertorio_item, get_repertorio_items, create_repertorio_item,
    update_repertorio_item, delete_repertorio_item, get_repertorio_by_group_and_year,
    get_available_years
)
from schemas.repertorio import RepertorioItem, RepertorioItemCreate, RepertorioItemUpdate
from models.user_local import User

router = APIRouter(prefix="/repertorio", tags=["repertorio"])

@router.get("/", response_model=List[RepertorioItem])
def read_repertorio_items(
    skip: int = 0,
    limit: int = 100,
    type_filter: Optional[str] = Query(None, description="Filter by type: Coral, Orquestra, or Setor"),
    active_only: bool = Query(True, description="Show only active items"),
    db: Session = Depends(get_db)
):
    """Lista itens do repertório com filtros por grupo"""
    try:
        items = get_repertorio_items(
            db, 
            skip=skip, 
            limit=limit, 
            type_filter=type_filter,
            active_only=active_only
        )
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar repertório: {str(e)}"
        )

@router.get("/by-group/{group_type}", response_model=List[RepertorioItem])
def read_repertorio_by_group(
    group_type: str,
    year: Optional[int] = Query(None, description="Filter by year"),
    db: Session = Depends(get_db)
):
    """Lista repertório específico por grupo (Coral/Orquestra/Setor)"""
    if group_type not in ["Coral", "Orquestra", "Setor"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Grupo deve ser: Coral, Orquestra ou Setor"
        )
    
    try:
        items = get_repertorio_by_group_and_year(db, group_type, year)
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar repertório do {group_type}: {str(e)}"
        )

@router.get("/years", response_model=List[int])
def read_available_years(
    group_type: Optional[str] = Query(None, description="Filter by group type"),
    db: Session = Depends(get_db)
):
    """Lista anos disponíveis no repertório"""
    try:
        years = get_available_years(db, group_type)
        return years
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar anos: {str(e)}"
        )

@router.post("/", response_model=RepertorioItem)
def create_repertorio_item_endpoint(
    item: RepertorioItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria um novo item do repertório"""
    try:
        return create_repertorio_item(db=db, item=item)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar item: {str(e)}"
        )

@router.get("/{item_id}", response_model=RepertorioItem)
def read_repertorio_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Busca um item específico do repertório"""
    db_item = get_repertorio_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Item do repertório não encontrado"
        )
    return db_item

@router.put("/{item_id}", response_model=RepertorioItem)
def update_repertorio_item_endpoint(
    item_id: int,
    item_update: RepertorioItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza um item do repertório"""
    try:
        db_item = update_repertorio_item(db, item_id=item_id, item_update=item_update)
        if db_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Item do repertório não encontrado"
            )
        return db_item
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar item: {str(e)}"
        )

@router.delete("/{item_id}")
def delete_repertorio_item_endpoint(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove um item do repertório"""
    try:
        db_item = delete_repertorio_item(db, item_id=item_id)
        if db_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Item do repertório não encontrado"
            )
        return {"message": "Item do repertório removido com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover item: {str(e)}"
        )
