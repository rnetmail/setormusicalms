# setormusicalms/backend/app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app import schemas
from app.database import get_db

# Create a new router object. This helps in organizing endpoints.
# It can be included in the main FastAPI app.
router = APIRouter()

@router.post("/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    - Checks if a user with the same username already exists.
    - If not, creates the user in the database.
    - Returns the created user's data.
    """
    db_user = crud.user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.user.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of users.

    - Supports pagination via `skip` and `limit` query parameters.
    """
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by their ID.

    - Raises a 404 error if the user is not found.
    """
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
