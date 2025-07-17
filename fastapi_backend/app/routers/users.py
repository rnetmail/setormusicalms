# fastapi_backend/app/routers/users.py
# Versão 13 17/07/2025 17:15
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# Importações de módulos da aplicação
import crud.user
import models.user
import schemas.user
from app.database import get_db
from auth.security import get_current_superuser

# Apenas superusuários podem acessar os endpoints deste router.
router = APIRouter(
    prefix="/users",
    tags=["Usuários"],
    dependencies=[Depends(get_current_superuser)]
)

@router.post("/", response_model=schemas.user.User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.user.UserCreate,
    db: Session = Depends(get_db)
):
    """Cria um novo usuário. Apenas superusuários podem executar esta ação."""
    try:
        if crud.user.get_user_by_username(db, username=user.username):
            raise HTTPException(status_code=400, detail="Usuário com este username já existe.")
        if crud.user.get_user_by_email(db, email=user.email):
            raise HTTPException(status_code=400, detail="Usuário com este e-mail já existe.")
        
        return crud.user.create_user(db=db, user=user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar usuário: {e}")

@router.get("/", response_model=List[schemas.user.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Lista todos os usuários. Apenas superusuários podem executar esta ação."""
    try:
        users = crud.user.get_users(db, skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao listar usuários: {e}")


@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Obtém os detalhes de um usuário específico pelo ID."""
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return db_user

@router.put("/{user_id}", response_model=schemas.user.User)
def update_user(
    user_id: int,
    user_update: schemas.user.UserUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza os dados de um usuário."""
    db_user_check = crud.user.get_user(db, user_id=user_id)
    if db_user_check is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    try:
        return crud.user.update_user(db, user_id=user_id, user_update=user_update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao atualizar usuário: {e}")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Apaga um usuário."""
    db_user = crud.user.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para exclusão.")
    return None
