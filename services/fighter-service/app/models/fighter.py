from sqlalchemy import create_engine, Column, String, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

Base = declarative_base()


class Fighter(Base):
    """مدل رزمنده"""
    __tablename__ = "fighters"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    national_id = Column(String(10), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    father_name = Column(String(50))
    birth_date = Column(Date)
    status = Column(String(20))  # 'alive', 'shaheed', 'janbaz', 'azadeh', 'missing'
    martyrdom_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Fighter {self.first_name} {self.last_name}>"


class FighterEvent(Base):
    """مدل رویدادهای رزمنده برای Event Sourcing"""
    __tablename__ = "fighter_events"
    
    id = Column(String, primary_key=True)
    fighter_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)
    payload = Column(JSONB, nullable=False)
    occurred_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<FighterEvent {self.event_type} for {self.fighter_id}>"
