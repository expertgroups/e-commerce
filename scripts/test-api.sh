#!/bin/bash

echo "🧪 تست API سامانه لشکر ۲۷"
echo "========================="

BASE_URL="http://localhost:8000/api/v1"

# تست سلامت سرویس
echo ""
echo "۱. بررسی سلامت سرویس..."
curl -s http://localhost:8000/health | jq .

# ثبت رزمنده جدید
echo ""
echo "۲. ثبت رزمنده جدید..."
RESPONSE=$(curl -s -X POST "$BASE_URL/fighters/register" \
  -H "Content-Type: application/json" \
  -d '{
    "national_id": "1234567890",
    "first_name": "علی",
    "last_name": "محمدی",
    "father_name": "حسن",
    "birth_date": "1960-01-01",
    "status": "shaheed"
  }')

echo $RESPONSE | jq .

# استخراج ID از پاسخ
FIGHTER_ID=$(echo $RESPONSE | jq -r '.id // empty')

if [ -n "$FIGHTER_ID" ]; then
    # دریافت اطلاعات رزمنده
    echo ""
    echo "۳. دریافت اطلاعات رزمنده..."
    curl -s "$BASE_URL/fighters/$FIGHTER_ID" | jq .
    
    # به‌روزرسانی اطلاعات
    echo ""
    echo "۴. به‌روزرسانی اطلاعات رزمنده..."
    curl -s -X PUT "$BASE_URL/fighters/$FIGHTER_ID" \
      -H "Content-Type: application/json" \
      -d '{
        "first_name": "حسین"
      }' | jq .
    
    # دریافت تاریخچه رویدادها
    echo ""
    echo "۵. دریافت تاریخچه رویدادها..."
    curl -s "$BASE_URL/fighters/$FIGHTER_ID/events" | jq .
    
    # لیست رزمندگان
    echo ""
    echo "۶. لیست رزمندگان..."
    curl -s "$BASE_URL/fighters?skip=0&limit=10" | jq .
else
    echo "⚠️ رزمنده‌ای ثبت نشد (احتمالاً تکراری است)"
fi

echo ""
echo "✅ تست‌ها به پایان رسید"
