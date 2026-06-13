from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
import uuid


class FighterBase(BaseModel):
    """پایه‌ی مشترک برای مدل‌های رزمنده"""
    national_id: str = Field(..., min_length=10, max_length=10)
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    father_name: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(alive|shaheed|janbaz|azadeh|missing)$")


class FighterCreate(FighterBase):
    """مدل ایجاد رزمنده جدید"""
    pass


class FighterUpdate(BaseModel):
    """مدل به‌روزرسانی رزمنده"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    father_name: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(alive|shaheed|janbaz|azadeh|missing)$")


class FighterResponse(FighterBase):
    """مدل پاسخ رزمنده"""
    id: uuid.UUID
    martyrdom_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FighterEvent(BaseModel):
    """مدل رویداد رزمنده"""
    event_id: str
    fighter_id: uuid.UUID
    event_type: str
    payload: dict
    occurred_at: datetime
