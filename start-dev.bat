@echo off
chcp 65001 >nul
echo ==========================================
echo   راه‌اندازی سامانه هوشمند لشکر ۲۷ (ویندوز)
echo ==========================================
echo.

REM بررسی نصب بودن Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [خطا] داکر نصب نیست یا در حال اجرا نیست.
    echo لطفاً Docker Desktop را نصب و اجرا کنید.
    pause
    exit /b 1
)

echo [اطلاعات] بررسی وضعیت داکر...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [خطا] سرویس داکر در حال اجرا نیست.
    echo لطفاً برنامه Docker Desktop را باز کنید و صبر کنید تا سبز شود.
    pause
    exit /b 1
)

echo [موفقیت] داکر آماده است.
echo.
echo [عملیات] در حال کشیدن ایمیج‌ها و ساخت کانتینرها...
echo (این مرحله بسته به سرعت اینترنت ممکن است چند دقیقه طول بکشد)
echo.

docker-compose up -d --build

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo   سامانه با موفقیت راه‌اندازی شد!
    echo ==========================================
    echo.
    echo دسترسی به پنل‌ها:
    echo - Swagger API: http://localhost:8000/docs
    echo - Neo4j Browser: http://localhost:7474
    echo - MinIO Console: http://localhost:9001
    echo - PostgreSQL: localhost:5432
    echo.
    echo برای مشاهده لاگ‌ها دستور زیر را بزنید:
    echo   docker-compose logs -f
    echo.
    echo برای توقف سامانه:
    echo   docker-compose down
    echo ==========================================
    pause
) else (
    echo.
    echo [خطا] در راه‌اندازی خطایی رخ داد. لاگ‌ها را بررسی کنید.
    pause
)
