@echo off
chcp 65001 >nul
echo ==========================================
echo   تست API سامانه لشکر ۲۷ (ویندوز)
echo ==========================================
echo.

REM بررسی curl
where curl >nul 2>&1
if %errorlevel% neq 0 (
    echo [خطا] دستور curl یافت نشد.
    echo لطفاً Git Bash یا WSL را نصب کنید یا از Postman استفاده نمایید.
    pause
    exit /b 1
)

echo [تست ۱] در حال ثبت رزمنده جدید...
curl -X POST http://localhost:8000/api/v1/fighters/register ^
  -H "Content-Type: application/json" ^
  -d "{\"national_id\": \"1234567890\", \"first_name\": \"علی\", \"last_name\": \"محمدی\", \"father_name\": \"حسن\", \"birth_date\": \"1960-01-01\", \"status\": \"shaheed\"}"
echo.
echo.

timeout /t 2 /nobreak >nul

echo [تست ۲] دریافت لیست رزمندگان...
curl -X GET http://localhost:8000/api/v1/fighters?limit=10^&offset=0
echo.
echo.

echo ==========================================
echo   تست‌ها تکمیل شد!
echo برای مشاهده مستندات به آدرس زیر بروید:
echo http://localhost:8000/docs
echo ==========================================
pause
