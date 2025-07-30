# /fastapi_backend/app/routers/recados.py
# v1.0 - 2025-07-30 01:50:25 - Corrige importações relativas e dependências.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.crud import recado as crud_recado
from app.crud import user as crud_user

router = APIRouter()

@router.post("/", response_model=schemas.Recado, status_code=status.HTTP_201_CREATED)
def create_recado(
    recado: schemas.RecadoCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Cria um novo recado. Apenas usuários autenticados podem criar recados.
    """
    return crud_recado.create_recado(db=db, recado=recado, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Recado])
def read_recados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista de recados.
    """
    recados = crud_recado.get_recados(db, skip=skip, limit=limit)
    return recados

@router.get("/{recado_id}", response_model=schemas.Recado)
def read_recado(recado_id: int, db: Session = Depends(get_db)):
    """
    Retorna um recado específico pelo ID.
    """
    db_recado = crud_recado.get_recado(db, recado_id=recado_id)
    if db_recado is None:
        raise HTTPException(status_code=404, detail="Recado not found")
    return db_recado

@router.delete("/{recado_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recado(
    recado_id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Deleta um recado. Apenas o autor do recado ou um administrador pode deletar.
    """
    db_recado = crud_recado.get_recado(db, recado_id=recado_id)
    if db_recado is None:
        raise HTTPException(status_code=404, detail="Recado not found")
    
    # Lógica de permissão (simplificada)
    if db_recado.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    crud_recado.delete_recado(db=db, recado_id=recado_id)
    return {"ok": True}
