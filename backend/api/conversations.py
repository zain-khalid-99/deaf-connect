from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import connection, crud, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Conversation])
def read_conversations(user_id: str, db: Session = Depends(connection.get_db)):
    return crud.get_conversations(db, user_id)

@router.post("/", response_model=schemas.Conversation)
def create_conversation(conversation: schemas.ConversationCreate, db: Session = Depends(connection.get_db)):
    return crud.create_conversation(db, conversation)

@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(connection.get_db)):
    crud.delete_conversation(db, conversation_id)
    return {"message": "Conversation deleted"}

@router.post("/messages", response_model=schemas.Message)
def create_message(message: schemas.MessageCreate, db: Session = Depends(connection.get_db)):
    return crud.create_message(db, message)

@router.get("/{conversation_id}/messages", response_model=List[schemas.Message])
def get_messages(conversation_id: int, db: Session = Depends(connection.get_db)):
    return crud.get_messages(db, conversation_id)

@router.put("/{conversation_id}/title")
def update_title(conversation_id: int, title: str, db: Session = Depends(connection.get_db)):
    return crud.update_conversation_title(db, conversation_id, title)
