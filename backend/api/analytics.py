from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import connection, crud

router = APIRouter()

@router.get("/{user_id}")
def get_user_analytics(user_id: str, db: Session = Depends(connection.get_db)):
    return crud.get_analytics(db, user_id)
