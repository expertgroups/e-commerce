from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """تنظیمات اصلی برنامه"""
    
    # Database
    DATABASE_URL: str = "postgresql://lashkar_admin:secure_password_123@localhost:5432/lashkar27_core"
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_TOPIC_FIGHTER_EVENTS: str = "fighter.events"
    KAFKA_TOPIC_DOCUMENT_EVENTS: str = "document.events"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    
    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minio_admin"
    MINIO_SECRET_KEY: str = "secure_password_123"
    MINIO_BUCKET: str = "documents"
    
    class Config:
        env_file = ".env"


settings = Settings()
