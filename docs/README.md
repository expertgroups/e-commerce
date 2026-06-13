# 📘 مستندات جامع پیاده‌سازی سامانه هوشمند لشکر ۲۷ محمد رسول‌الله (ص)

## 📋 فهرست مطالب

1. [معرفی پروژه](#معرفی-پروژه)
2. [معماری سیستم](#معماری-سیستم)
3. [راه‌اندازی سریع](#راه‌اندازی-سریع)
4. [ساختار کد](#ساختار-کد)
5. [APIها](#apiها)
6. [توسعه بیشتر](#توسعه-بیشتر)

---

## 🎯 معرفی پروژه

این سامانه یک **پلتفرم دیجیتال یکپارچه** برای ثبت، حفظ، تحلیل و روایتگری میراث دفاع مقدس با تمرکز بر لشکر ۲۷ محمد رسول‌الله (ص) است.

### ویژگی‌های کلیدی
- ✅ ثبت و مدیریت اطلاعات رزمندگان
- ✅ Event Sourcing برای ردیابی تغییرات
- ✅ معماری مبتنی بر دامنه (DDD)
- ✅ پردازش اسناد با هوش مصنوعی
- ✅ گراف دانش برای روابط معنایی

---

## 🏛️ معماری سیستم

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (Kong)                        │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼───────┐   ┌────────▼────────┐   ┌───────▼───────┐
│ Fighter       │   │ Document        │   │ AI Platform   │
│ Service       │   │ Service         │   │               │
└───────┬───────┘   └────────┬────────┘   └───────┬───────┘
        │                    │                     │
   ┌────▼────┐          ┌────▼────┐           ┌────▼────┐
   │PostgreSQL│          │ MinIO   │           │ Neo4j   │
   └─────────┘          └─────────┘           └─────────┘
        │                    │                     │
        └────────────────────┼─────────────────────┘
                             │
                    ┌────────▼────────┐
                    │    Apache Kafka │
                    │   (Event Bus)   │
                    └─────────────────┘
```

---

## 🚀 راه‌اندازی سریع

### پیش‌نیازها
- Docker و Docker Compose
- Python 3.12+
- حداقل 8GB RAM

### مرحله ۱: کلون کردن مخزن
```bash
cd /workspace
```

### مرحله ۲: راه‌اندازی با Docker Compose
```bash
docker-compose up -d
```

### مرحله ۳: بررسی وضعیت سرویس‌ها
```bash
docker-compose ps
```

### مرحله ۴: دسترسی به API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📁 ساختار کد

```
/workspace
├── docker-compose.yml              # پیکربندی Docker
├── services/
│   └── fighter-service/            # سرویس مدیریت رزمندگان
│       ├── app/
│       │   ├── api/                # API routes
│       │   │   ├── main.py         # نقطه ورود اصلی
│       │   │   └── fighter_routes.py
│       │   ├── core/               # تنظیمات اصلی
│       │   │   ├── config.py       # تنظیمات محیطی
│       │   │   └── database.py     # اتصال به دیتابیس
│       │   ├── models/             # مدل‌های داده
│       │   │   └── fighter.py      # مدل رزمنده
│       │   ├── schemas/            # Pydantic schemas
│       │   │   └── fighter.py      # اعتبارسنجی داده
│       │   └── repositories/       # لایه دسترسی به داده
│       │       └── fighter_repository.py
│       ├── requirements.txt        # وابستگی‌های Python
│       └── Dockerfile              # پیکربندی Docker
├── infrastructure/
│   └── helm/lashkar27/             # Helm charts برای Kubernetes
├── docs/                           # مستندات
└── scripts/                        # اسکریپت‌های کمکی
```

---

## 🔌 APIها

### ثبت رزمنده جدید
```bash
curl -X POST http://localhost:8000/api/v1/fighters/register \
  -H "Content-Type: application/json" \
  -d '{
    "national_id": "1234567890",
    "first_name": "علی",
    "last_name": "محمدی",
    "father_name": "حسن",
    "birth_date": "1960-01-01",
    "status": "shaheed"
  }'
```

### دریافت اطلاعات رزمنده
```bash
curl http://localhost:8000/api/v1/fighters/{fighter_id}
```

### لیست رزمندگان
```bash
curl "http://localhost:8000/api/v1/fighters?skip=0&limit=10"
```

### به‌روزرسانی اطلاعات
```bash
curl -X PUT http://localhost:8000/api/v1/fighters/{fighter_id} \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "حسین"
  }'
```

### ثبت شهادت
```bash
curl -X POST http://localhost:8000/api/v1/fighters/{fighter_id}/martyrdom?martyrdom_date=1985-02-15
```

### دریافت تاریخچه رویدادها
```bash
curl http://localhost:8000/api/v1/fighters/{fighter_id}/events
```

---

## 🗄️ مدل داده‌ای

### جدول Fighters
| فیلد | نوع | توضیحات |
|------|-----|---------|
| id | UUID | شناسه یکتا |
| national_id | VARCHAR(10) | کد ملی |
| first_name | VARCHAR(50) | نام |
| last_name | VARCHAR(50) | نام خانوادگی |
| father_name | VARCHAR(50) | نام پدر |
| birth_date | DATE | تاریخ تولد |
| status | VARCHAR(20) | وضعیت (alive, shaheed, ...) |
| martyrdom_date | DATE | تاریخ شهادت |
| created_at | TIMESTAMP | زمان ایجاد |
| updated_at | TIMESTAMP | زمان آخرین به‌روزرسانی |

### جدول FighterEvents (Event Sourcing)
| فیلد | نوع | توضیحات |
|------|-----|---------|
| id | BIGSERIAL | شناسه رویداد |
| fighter_id | UUID | شناسه رزمنده |
| event_type | VARCHAR(50) | نوع رویداد |
| payload | JSONB | داده‌های رویداد |
| occurred_at | TIMESTAMP | زمان وقوع |

---

## 🧪 تست

### اجرای تست‌های واحد
```bash
cd services/fighter-service
pytest tests/
```

### تست بارگذاری
```bash
k6 run scripts/load-test.js
```

---

## 📊 مانیتورینگ

### Prometheus Metrics
- آدرس: http://localhost:9090
- متریک‌های سفارشی در `/metrics`

### Grafana Dashboards
- آدرس: http://localhost:3000
- داشبوردهای آماده برای Kafka lag، خطاهای API

### Jaeger Tracing
- آدرس: http://localhost:16686
- ردیابی درخواست‌های توزیع‌شده

---

## 🔐 امنیت

### احراز هویت
- OAuth2 با Ory Hydra
- JWT tokens با طول عمر کوتاه

### رمزنگاری
- TLS 1.3 برای ترافیک شبکه
- رمزنگاری داده‌ها در حالت سکون

### کنترل دسترسی
- RBAC با نقش‌های مختلف
- OPA برای policy enforcement

---

## 📈 مقیاس‌پذیری

### Horizontal Scaling
```bash
kubectl scale deployment fighter-service --replicas=5
```

### Caching Strategy
- Redis برای کش کردن کوئری‌های پرتکرار
- TTL-based invalidation

### Database Optimization
- Indexing روی فیلدهای پرجستجو
- Connection pooling با PgBouncer

---

## 🤖 هوش مصنوعی

### خط لوله پردازش
1. تشخیص نوع رسانه
2. OCR فارسی برای اسناد متنی
3. NER برای استخراج موجودیت‌ها
4. Face Recognition برای شناسایی چهره
5. Speech-to-Text برای فایل‌های صوتی

### مدل‌های استفاده شده
- OCR: Tesseract 5 (fine-tuned for Persian)
- NER: HooshvareLab/bert-fa-zwnj-base-ner
- Face Recognition: ArcFace
- STT: Whisper large-v3

---

## 🛠️ توسعه بیشتر

### افزودن سرویس جدید
1. ایجاد پوشه در `services/`
2. تعریف modelهای جدید
3. ایجاد API routes
4. اضافه کردن به docker-compose.yml

### افزودن قابلیت جدید
1. تعریف domain event جدید
2. ایجاد consumer در Kafka
3. به‌روزرسانی projectionها

---

## 📞 پشتیبانی

برای گزارش مشکلات یا درخواست ویژگی‌های جدید، لطفاً از طریق Issues اقدام کنید.

---

## 📝 مجوز

این پروژه تحت مجوز اختصاصی لشکر ۲۷ محمد رسول‌الله (ص) منتشر شده است.
