"""
Module: analytics.py
Purpose: FastAPI router for analytics endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import connection, crud, schemas  # FIX: added missing 'schemas' import

router = APIRouter()

@router.get("/{user_id}")
def get_user_analytics(user_id: str, db: Session = Depends(connection.get_db)):
    return crud.get_analytics(db, user_id)

@router.get("/{user_id}/history")
def get_user_detection_history(user_id: str, limit: int = 50, db: Session = Depends(connection.get_db)):
    return crud.get_detection_history(db, user_id, limit)

@router.post("/detection")
def save_detection(history: schemas.DetectionHistoryCreate, db: Session = Depends(connection.get_db)):
    return crud.create_detection_history(db, history)
