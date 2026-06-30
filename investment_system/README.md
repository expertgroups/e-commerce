# Investment Intelligence System (IIS) v4.0

## 🎯 معرفی سیستم

سیستم هوشمند مدیریت سرمایه‌گذاری برای بورس ایران با قابلیت‌های:
- جمع‌آوری خودکار داده‌ها از کدال و بورس تهران
- محاسبه شاخص‌های بنیادی و تکنیکال
- پیش‌بینی قیمت با مدل‌های یادگیری ماشین
- بهینه‌سازی پرتفوی با الگوریتم‌های فراابتکاری
- داشبورد تعاملی برای تحلیل و نظارت

## 📁 ساختار پروژه

```
investment_system/
├── config/              # فایل‌های پیکربندی
├── src/                 # کدهای اصلی
│   ├── data_pipeline/   # خط لوله داده
│   ├── ml_models/       # مدل‌های یادگیری ماشین
│   ├── portfolio/       # بهینه‌سازی پرتفوی
│   ├── api/             # API FastAPI
│   └── utils/           # توابع کمکی
├── dashboard/           # داشبورد Streamlit
├── scripts/             # اسکریپت‌های اجرایی
├── tests/               # تست‌ها
└── docs/                # مستندات
```

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.10+
- PostgreSQL 14+
- Redis 6+
- Docker & Docker Compose (اختیاری)

### نصب با Docker (توصیه می‌شود)

```bash
docker-compose up -d
```

### نصب دستی

1. **کلون کردن پروژه:**
```bash
git clone <repository-url>
cd investment_system
```

2. **نصب وابستگی‌ها:**
```bash
pip install -r requirements.txt
```

3. **تنظیم متغیرهای محیطی:**
```bash
cp .env.example .env
# ویرایش فایل .env و تنظیم مقادیر
```

4. **راه‌اندازی پایگاه داده:**
```bash
python -m src.data_pipeline.storage.database init
```

5. **اجرای API:**
```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
```

6. **اجرای داشبورد:**
```bash
streamlit run dashboard/app.py
```

## 📊 ویژگی‌ها

### Data Pipeline
- خزنده کدال برای صورت‌های مالی
- خزنده بورس تهران برای قیمت‌ها
- خزنده داده‌های کلان اقتصادی
- پاکسازی و اعتبارسنجی داده‌ها
- محاسبه ۵۰+ ویژگی بنیادی و تکنیکال

### ML Models
- XGBoost با بهینه‌سازی Optuna
- LSTM/GRU برای سری‌های زمانی
- Ensemble Model برای دقت بالاتر
- Backtesting کامل
- تفسیرپذیری با SHAP

### Portfolio Optimization
- الگوریتم ژنتیک چندهدفه
- مدیریت ریسک (VaR, CVaR)
- تحلیل عملکرد پرتفوی

### API
- RESTful API با FastAPI
- احراز هویت JWT
- Rate Limiting
- مستندات Swagger

### Dashboard
- تحلیل بازار
- مدیریت پرتفوی
- پیش‌بینی‌ها
- گزارش‌گیری

## 📝 مستندات

- [مستندات API](docs/api/api_reference.md)
- [کارت مدل‌ها](docs/models/)
- [راهنمای کاربر](docs/user_guides/)

## 🧪 تست

```bash
pytest tests/ -v --cov=src
```

## 📄 لایسنس

MIT License

## 🤝 مشارکت

لطفاً برای مشارکت، راهنمای CONTRIBUTING.md را مطالعه کنید.
