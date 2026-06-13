from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid

from app.core.database import get_db
from app.schemas.fighter import FighterCreate, FighterUpdate, FighterResponse, FighterEvent as FighterEventSchema
from app.repositories.fighter_repository import FighterRepository


router = APIRouter(prefix="/api/v1/fighters", tags=["fighters"])


@router.post("/register", response_model=FighterResponse, status_code=status.HTTP_201_CREATED)
def register_fighter(fighter_data: FighterCreate, db: Session = Depends(get_db)):
    """ثبت رزمنده جدید"""
    repo = FighterRepository()
    try:
        # بررسی تکراری نبودن کد ملی
        existing = repo.get_fighter_by_national_id(fighter_data.national_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="رزمنده با این کد ملی قبلاً ثبت شده است"
            )
        
        fighter = repo.create_fighter(fighter_data)
        return fighter
    finally:
        repo.db.close()


@router.get("/{fighter_id}", response_model=FighterResponse)
def get_fighter(fighter_id: str, db: Session = Depends(get_db)):
    """دریافت اطلاعات رزمنده بر اساس ID"""
    repo = FighterRepository()
    try:
        fighter = repo.get_fighter_by_id(uuid.UUID(fighter_id))
        if not fighter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="رزمنده یافت نشد"
            )
        return fighter
    finally:
        repo.db.close()


@router.get("", response_model=List[FighterResponse])
def list_fighters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """دریافت لیست رزمندگان با pagination"""
    repo = FighterRepository()
    try:
        fighters = repo.get_all_fighters(skip=skip, limit=limit)
        return fighters
    finally:
        repo.db.close()


@router.put("/{fighter_id}", response_model=FighterResponse)
def update_fighter(fighter_id: str, fighter_data: FighterUpdate, db: Session = Depends(get_db)):
    """به‌روزرسانی اطلاعات رزمنده"""
    repo = FighterRepository()
    try:
        fighter = repo.update_fighter(uuid.UUID(fighter_id), fighter_data)
        if not fighter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="رزمنده یافت نشد"
            )
        return fighter
    finally:
        repo.db.close()


@router.post("/{fighter_id}/martyrdom", response_model=FighterResponse)
def register_martyrdom(fighter_id: str, martyrdom_date: datetime, db: Session = Depends(get_db)):
    """ثبت شهادت رزمنده"""
    repo = FighterRepository()
    try:
        fighter = repo.register_martyrdom(uuid.UUID(fighter_id), martyrdom_date)
        if not fighter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="رزمنده یافت نشد"
            )
        return fighter
    finally:
        repo.db.close()


@router.get("/{fighter_id}/events", response_model=List[FighterEventSchema])
def get_fighter_events(fighter_id: str, db: Session = Depends(get_db)):
    """دریافت تاریخچه رویدادهای رزمنده"""
    repo = FighterRepository()
    try:
        events = repo.get_fighter_events(uuid.UUID(fighter_id))
        return events
    finally:
        repo.db.close()
