from app.core.database import SessionLocal
from app.models.fighter import Fighter, FighterEvent
from app.schemas.fighter import FighterCreate, FighterUpdate
from typing import List, Optional
import uuid
from datetime import datetime


class FighterRepository:
    """repository برای مدیریت عملیات رزمنده"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def create_fighter(self, fighter_data: FighterCreate) -> Fighter:
        """ایجاد رزمنده جدید"""
        fighter = Fighter(**fighter_data.model_dump())
        self.db.add(fighter)
        
        # ثبت رویداد ایجاد
        event = FighterEvent(
            id=str(uuid.uuid4()),
            fighter_id=fighter.id,
            event_type="FighterRegistered",
            payload={
                "national_id": fighter.national_id,
                "first_name": fighter.first_name,
                "last_name": fighter.last_name,
                "status": fighter.status
            },
            occurred_at=datetime.utcnow()
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(fighter)
        return fighter
    
    def get_fighter_by_id(self, fighter_id: uuid.UUID) -> Optional[Fighter]:
        """دریافت رزمنده بر اساس ID"""
        return self.db.query(Fighter).filter(Fighter.id == fighter_id).first()
    
    def get_fighter_by_national_id(self, national_id: str) -> Optional[Fighter]:
        """دریافت رزمنده بر اساس کد ملی"""
        return self.db.query(Fighter).filter(Fighter.national_id == national_id).first()
    
    def get_all_fighters(self, skip: int = 0, limit: int = 100) -> List[Fighter]:
        """دریافت همه رزمندگان با pagination"""
        return self.db.query(Fighter).offset(skip).limit(limit).all()
    
    def update_fighter(self, fighter_id: uuid.UUID, fighter_data: FighterUpdate) -> Optional[Fighter]:
        """به‌روزرسانی اطلاعات رزمنده"""
        fighter = self.get_fighter_by_id(fighter_id)
        if not fighter:
            return None
        
        update_data = fighter_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(fighter, field, value)
        
        # ثبت رویداد به‌روزرسانی
        event = FighterEvent(
            id=str(uuid.uuid4()),
            fighter_id=fighter.id,
            event_type="FighterUpdated",
            payload=update_data,
            occurred_at=datetime.utcnow()
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(fighter)
        return fighter
    
    def register_martyrdom(self, fighter_id: uuid.UUID, martyrdom_date: datetime) -> Optional[Fighter]:
        """ثبت شهادت رزمنده"""
        fighter = self.get_fighter_by_id(fighter_id)
        if not fighter:
            return None
        
        fighter.status = "shaheed"
        fighter.martyrdom_date = martyrdom_date
        
        # ثبت رویداد شهادت
        event = FighterEvent(
            id=str(uuid.uuid4()),
            fighter_id=fighter.id,
            event_type="MartyrdomRegistered",
            payload={
                "martyrdom_date": martyrdom_date.isoformat()
            },
            occurred_at=datetime.utcnow()
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(fighter)
        return fighter
    
    def get_fighter_events(self, fighter_id: uuid.UUID) -> List[FighterEvent]:
        """دریافت تاریخچه رویدادهای رزمنده"""
        return self.db.query(FighterEvent).filter(FighterEvent.fighter_id == fighter_id).all()
