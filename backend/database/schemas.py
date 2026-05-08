from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    sender: str
    raw_words: Optional[str] = None
    translated_sentence: str
    confidence: Optional[float] = 0.0

class MessageCreate(MessageBase):
    conversation_id: int

class Message(MessageBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    title: str = "New Conversation"

class ConversationCreate(ConversationBase):
    user_id: str

class Conversation(ConversationBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[Message] = []
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    id: str

class User(UserBase):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

class SettingBase(BaseModel):
    theme: str = "dark"
    speech_rate: float = 1.0
    speech_volume: float = 1.0
    auto_speak: bool = True
    camera_index: int = 0

class SettingUpdate(SettingBase):
    pass

class Setting(SettingBase):
    id: int
    user_id: str
    class Config:
        from_attributes = True

class AnalyticBase(BaseModel):
    total_words: int
    avg_confidence: float
    session_duration: int

class AnalyticCreate(AnalyticBase):
    user_id: str

class Analytic(AnalyticBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
