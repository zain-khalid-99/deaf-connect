from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import models, schemas

# User CRUD
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Also create default settings
    default_settings = models.Setting(user_id=db_user.id)
    db.add(default_settings)
    db.commit()
    return db_user

# Conversation CRUD
def get_conversations(db: Session, user_id: str):
    return db.query(models.Conversation).filter(models.Conversation.user_id == user_id).order_by(models.Conversation.updated_at.desc()).all()

def create_conversation(db: Session, conversation: schemas.ConversationCreate):
    db_conv = models.Conversation(**conversation.model_dump())
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv

def delete_conversation(db: Session, conversation_id: int):
    db_conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if db_conv:
        db.delete(db_conv)
        db.commit()
    return db_conv

def update_conversation_title(db: Session, conversation_id: int, title: str):
    db_conv = db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()
    if db_conv:
        db_conv.title = title
        db.commit()
        db.refresh(db_conv)
    return db_conv

# Message CRUD
def create_message(db: Session, message: schemas.MessageCreate):
    db_msg = models.Message(**message.model_dump())
    db.add(db_msg)
    # Update conversation updated_at
    db_conv = db.query(models.Conversation).filter(models.Conversation.id == message.conversation_id).first()
    if db_conv:
        db_conv.updated_at = func.now()
    db.commit()
    db.refresh(db_msg)
    return db_msg

def get_messages(db: Session, conversation_id: int):
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).order_by(models.Message.created_at.asc()).all()

# Settings CRUD
def get_settings(db: Session, user_id: str):
    return db.query(models.Setting).filter(models.Setting.user_id == user_id).first()

def update_settings(db: Session, user_id: str, settings_update: schemas.SettingUpdate):
    db_settings = db.query(models.Setting).filter(models.Setting.user_id == user_id).first()
    if not db_settings:
        db_settings = models.Setting(user_id=user_id, **settings_update.model_dump(exclude_unset=True))
        db.add(db_settings)
    else:
        for key, value in settings_update.model_dump(exclude_unset=True).items():
            setattr(db_settings, key, value)
    db.commit()
    db.refresh(db_settings)
    return db_settings

# Analytics CRUD
def get_analytics(db: Session, user_id: str):
    # Total chats
    total_chats = db.query(models.Conversation).filter(models.Conversation.user_id == user_id).count()
    
    # Total messages/words
    total_messages = db.query(models.Message).join(models.Conversation).filter(models.Conversation.user_id == user_id).count()
    
    # Average confidence
    avg_confidence = db.query(func.avg(models.Message.confidence)).join(models.Conversation).filter(models.Conversation.user_id == user_id).scalar() or 0.0
    
    return {
        "total_chats": total_chats,
        "total_messages": total_messages,
        "avg_confidence": round(avg_confidence, 2)
    }

def create_analytic_entry(db: Session, analytic: schemas.AnalyticCreate):
    db_analytic = models.Analytic(**analytic.model_dump())
    db.add(db_analytic)
    db.commit()
    db.refresh(db_analytic)
    return db_analytic

# Detection History CRUD
def create_detection_history(db: Session, history: schemas.DetectionHistoryCreate):
    db_history = models.DetectionHistory(**history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

def get_detection_history(db: Session, user_id: str, limit: int = 100):
    return db.query(models.DetectionHistory).filter(models.DetectionHistory.user_id == user_id).order_by(models.DetectionHistory.timestamp.desc()).limit(limit).all()

# Model Prediction CRUD
def create_model_prediction(db: Session, prediction: schemas.ModelPredictionCreate):
    db_pred = models.ModelPrediction(**prediction.model_dump())
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred

# Log CRUD
def create_log(db: Session, log: schemas.LogCreate):
    db_log = models.Log(**log.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
