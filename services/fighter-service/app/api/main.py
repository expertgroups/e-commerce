from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.fighter_routes import router as fighter_router
from app.core.database import init_db
from app.core.config import settings


app = FastAPI(
    title="سامانه هوشمند لشکر ۲۷ محمد رسول‌الله (ص)",
    description="پلتفرم دیجیتال یکپارچه برای ثبت، حفظ، تحلیل و روایتگری میراث دفاع مقدس",
    version="1.0.0"
)

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # در production محدود شود
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ثبت routerها
app.include_router(fighter_router)


@app.on_event("startup")
async def startup_event():
    """ایجاد جداول پایگاه داده در زمان راه‌اندازی"""
    init_db()
    print("✅ سامانه با موفقیت راه‌اندازی شد")
    print(f"📊 Kafka: {settings.KAFKA_BOOTSTRAP_SERVERS}")
    print(f"🗄️  Database: {settings.DATABASE_URL}")


@app.get("/")
async def root():
    """صفحه اصلی API"""
    return {
        "message": "سامانه هوشمند لشکر ۲۷ محمد رسول‌الله (ص)",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """بررسی سلامت سرویس"""
    return {"status": "healthy"}
