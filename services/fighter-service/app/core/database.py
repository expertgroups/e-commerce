from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.fighter import Base

# ایجاد اتصال به پایگاه داده
engine = create_engine(settings.DATABASE_URL)

# SessionLocal برای مدیریت sessionها
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency برای دریافت session دیتابیس"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """ایجاد جداول در پایگاه داده"""
    Base.metadata.create_all(bind=engine)
