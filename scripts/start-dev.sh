#!/bin/bash

echo "🚀 راه‌اندازی سامانه هوشمند لشکر ۲۷ محمد رسول‌الله (ص)"
echo "================================================"

# بررسی Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker نصب نیست. لطفاً Docker را نصب کنید."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose نصب نیست. لطفاً Docker Compose را نصب کنید."
    exit 1
fi

echo "✅ پیش‌نیازها بررسی شد"

# راه‌اندازی سرویس‌ها
cd /workspace
docker-compose up -d

echo ""
echo "⏳ انتظار برای راه‌اندازی سرویس‌ها..."
sleep 10

# بررسی وضعیت
echo ""
echo "📊 وضعیت سرویس‌ها:"
docker-compose ps

echo ""
echo "✅ سامانه با موفقیت راه‌اندازی شد!"
echo ""
echo "🔗 دسترسی به سرویس‌ها:"
echo "   - Fighter Service API: http://localhost:8000"
echo "   - Swagger UI: http://localhost:8000/docs"
echo "   - PostgreSQL: localhost:5432"
echo "   - Kafka: localhost:9092"
echo "   - Neo4j: http://localhost:7474"
echo "   - MinIO Console: http://localhost:9001"
echo "   - Redis: localhost:6379"
echo ""
echo "📝 برای مشاهده لاگ‌ها:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 برای توقف سرویس‌ها:"
echo "   docker-compose down"
