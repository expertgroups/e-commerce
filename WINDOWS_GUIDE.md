# 🚀 راهنمای راه‌اندازی در ویندوز

## پیش‌نیازها

### ۱. نصب Docker Desktop (الزامی)
1. به آدرس [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) بروید
2. نسخه Windows را دانلود و نصب کنید
3. پس از نصب، سیستم را ریستارت کنید
4. برنامه **Docker Desktop** را اجرا کنید
5. صبر کنید تا علامت سبز رنگ پایین سمت چپ ظاهر شود (به معنای آماده بودن است)

### ۲. نصب Git (اختیاری - برای دسترسی راحت‌تر)
- از [git-scm.com](https://git-scm.com/download/win) دانلود و نصب کنید
- این کار باعث می‌شود `curl` و سایر ابزارهای خط فرمان در دسترس باشند

---

## 🎯 راه‌اندازی سریع (۳ مرحله ساده)

### مرحله ۱: باز کردن PowerShell یا Command Prompt
- کلید `Win + R` را بزنید
- تایپ کنید `powershell` و Enter بزنید
- یا در منوی Start، **Command Prompt** را جستجو کنید

### مرحله ۲: رفتن به پوشه پروژه
```powershell
cd C:\path\to\workspace
```
(به جای `C:\path\to\workspace` مسیر واقعی پوشه project را وارد کنید)

### مرحله ۳: اجرای سامانه
```powershell
.\start-dev.bat
```

یا اگر از PowerShell استفاده می‌کنید:
```powershell
.\start-dev.ps1
```

---

## 🔍 مشاهده وضعیت سرویس‌ها

### مشاهده لاگ‌ها:
```powershell
docker-compose logs -f
```

### مشاهده وضعیت کانتینرها:
```powershell
docker ps
```

---

## 🌐 دسترسی به پنل‌ها

| سرویس | آدرس | توضیحات |
|-------|------|---------|
| **Swagger UI** | http://localhost:8000/docs | مستندات زنده API |
| **Fighter API** | http://localhost:8000/api/v1/fighters | API رزمندگان |
| **Neo4j Browser** | http://localhost:7474 | مدیریت گراف دانش |
| **MinIO Console** | http://localhost:9001 | مدیریت فایل‌ها |
| **PostgreSQL** | localhost:5432 | پایگاه داده |

---

## 🧪 تست API

### روش ۱: استفاده از فایل تست خودکار
```powershell
.\test-api.bat
```

### روش ۲: استفاده از Swagger UI
1. مرورگر را باز کنید
2. به آدرس http://localhost:8000/docs بروید
3. روی `POST /api/v1/fighters/register` کلیک کنید
4. دکمه `Try it out` را بزنید
5. مقادیر نمونه را وارد و Execute کنید

### روش ۳: استفاده از PowerShell
```powershell
curl -X POST http://localhost:8000/api/v1/fighters/register `
  -H "Content-Type: application/json" `
  -d '{
    "national_id": "1234567890",
    "first_name": "علی",
    "last_name": "محمدی",
    "father_name": "حسن",
    "birth_date": "1960-01-01",
    "status": "shaheed"
  }'
```

### روش ۴: استفاده از Postman
1. Postman را دانلود و نصب کنید
2. یک درخواست جدید بسازید
3. Method را `POST` انتخاب کنید
4. URL: `http://localhost:8000/api/v1/fighters/register`
5. Body → raw → JSON
6. کد زیر را وارد کنید:
```json
{
  "national_id": "1234567890",
  "first_name": "علی",
  "last_name": "محمدی",
  "father_name": "حسن",
  "birth_date": "1960-01-01",
  "status": "shaheed"
}
```

---

## ⏹️ توقف سامانه

```powershell
docker-compose down
```

برای حذف کامل داده‌ها:
```powershell
docker-compose down -v
```

---

## ❓ رفع مشکلات رایج

### مشکل: Docker در حال اجرا نیست
**راه حل:**
1. برنامه Docker Desktop را از منوی Start باز کنید
2. صبر کنید تا کاملاً بارگذاری شود (علامت سبز ظاهر شود)
3. دوباره امتحان کنید

### مشکل: پورت‌ها اشغال هستند
**راه حل:**
```powershell
# مشاهده برنامه‌های در حال استفاده از پورت
netstat -ano | findstr :8000
netstat -ano | findstr :5432

# بستن برنامه مزاحم یا تغییر پورت در docker-compose.yml
```

### مشکل: دسترسی denied در PowerShell
**راه حل:**
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\start-dev.bat
```

### مشکل: خطای encoding فارسی
**راه حل:**
- فایل‌های `.bat` با encoding UTF-8 ذخیره شده‌اند
- اگر حروف فارسی درست نمایش داده نمی‌شوند، CMD را با فونت `Lucida Console` اجرا کنید

---

## 📊 منابع سیستم مورد نیاز

| منبع | حداقل | پیشنهادی |
|------|-------|----------|
| RAM | 8 GB | 16 GB |
| CPU | 4 cores | 8 cores |
| فضای دیسک | 10 GB | 20 GB SSD |
| اینترنت | - | برای دانلود اولیه ایمیج‌ها |

---

## 🔄 به‌روزرسانی

```powershell
# کشیدن آخرین تغییرات کد
git pull

# ساخت مجدد و راه‌اندازی
docker-compose up -d --build
```

---

## 📞 پشتیبانی

در صورت بروز مشکل:
1. لاگ‌ها را بررسی کنید: `docker-compose logs`
2. وضعیت کانتینرها را ببینید: `docker ps -a`
3. مطمئن شوید Docker Desktop در حال اجراست

---

## ✅ چک‌لیست نهایی

- [ ] Docker Desktop نصب و در حال اجراست
- [ ] به پوشه پروژه رفته‌اید
- [ ] دستور `.\start-dev.bat` را اجرا کرده‌اید
- [ ] پیام "سامانه با موفقیت راه‌اندازی شد" را دیده‌اید
- [ ] به آدرس http://localhost:8000/docs دسترسی دارید
- [ ] می‌توانید یک رزمنده ثبت کنید

**آماده شروع هستید!** 🎉
