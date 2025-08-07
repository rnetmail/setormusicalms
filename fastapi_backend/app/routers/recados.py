# /fastapi_backend/app/routers/recados.py
# v2.1 - 2025-08-07 - Corrige importações para absolutas.

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# --- INÍCIO DA CORREÇÃO ---
# Importações absolutas a partir da raiz do projeto 'app'
from app.schemas import recado as recado_schemas, user as user_schemas
from app.database import get_db
from app.crud import recado as crud_recado, user as crud_user
# --- FIM DA CORREÇÃO ---

router = APIRouter(prefix="/api/recados", tags=["Recados"])

@router.post("/", response_model=recado_schemas.RecadoItem, status_code=status.HTTP_201_CREATED)
def create_recado(
    recado: recado_schemas.RecadoItemCreate, 
    db: Session = Depends(get_db), 
    current_user: user_schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Cria um novo recado. Apenas usuários autenticados podem criar recados.
    """
    return crud_recado.create_recado(db=db, recado=recado, user_id=current_user.id)

@router.get("/", response_model=List[recado_schemas.RecadoItem])
def read_recados(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista de recados.
    """
    recados = crud_recado.get_recados(db, skip=skip, limit=limit)
    return recados

@router.get("/{recado_id}", response_model=recado_schemas.RecadoItem)
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
    current_user: user_schemas.User = Depends(crud_user.get_current_active_user)
):
    """
    Deleta um recado. Apenas o autor do recado ou um administrador pode deletar.
    """
    db_recado = crud_recado.get_recado(db, recado_id=recado_id)
    if db_recado is None:
        raise HTTPException(status_code=404, detail="Recado not found")
    
    if db_recado.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    crud_recado.delete_recado(db=db, recado_id=recado_id)
    return {"ok": True}
