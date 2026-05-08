from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import connection, crud, schemas

router = APIRouter()

@router.post("/login", response_model=schemas.User)
def login(user_data: schemas.UserCreate, db: Session = Depends(connection.get_db)):
    db_user = crud.get_user(db, user_data.id)
    if not db_user:
        return crud.create_user(db, user_data)
    return db_user

@router.get("/me/{user_id}", response_model=schemas.User)
def get_me(user_id: str, db: Session = Depends(connection.get_db)):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
