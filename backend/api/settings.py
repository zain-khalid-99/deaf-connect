from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import connection, crud, schemas

router = APIRouter()

@router.get("/{user_id}", response_model=schemas.Setting)
def get_user_settings(user_id: str, db: Session = Depends(connection.get_db)):
    settings = crud.get_settings(db, user_id)
    if not settings:
        # Create default settings if not exists
        return crud.update_settings(db, user_id, schemas.SettingUpdate())
    return settings

@router.put("/{user_id}", response_model=schemas.Setting)
def update_user_settings(user_id: str, settings_update: schemas.SettingUpdate, db: Session = Depends(connection.get_db)):
    return crud.update_settings(db, user_id, settings_update)
