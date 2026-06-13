# PowerShell Script for Windows
# Execute: .\start-dev.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  راه‌اندازی سامانه هوشمند لشکر ۲۷ (ویندوز)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# بررسی نصب بودن Docker
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "داکر نصب نیست"
    }
    Write-Host "[موفقیت] داکر نصب است: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "[خطا] داکر نصب نیست یا در حال اجرا نیست." -ForegroundColor Red
    Write-Host "لطفاً Docker Desktop را نصب و اجرا کنید." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# بررسی وضعیت Docker Daemon
try {
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "سرویس داکر در حال اجرا نیست"
    }
    Write-Host "[موفقیت] سرویس داکر آماده است." -ForegroundColor Green
} catch {
    Write-Host "[خطا] سرویس داکر در حال اجرا نیست." -ForegroundColor Red
    Write-Host "لطفاً برنامه Docker Desktop را باز کنید و صبر کنید تا سبز شود." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[عملیات] در حال کشیدن ایمیج‌ها و ساخت کانتینرها..." -ForegroundColor Cyan
Write-Host "(این مرحله بسته به سرعت اینترنت ممکن است چند دقیقه طول بکشد)" -ForegroundColor Gray
Write-Host ""

# اجرای docker-compose
docker-compose up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "  سامانه با موفقیت راه‌اندازی شد!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "دسترسی به پنل‌ها:" -ForegroundColor Cyan
    Write-Host "  - Swagger API: http://localhost:8000/docs" -ForegroundColor White
    Write-Host "  - Neo4j Browser: http://localhost:7474" -ForegroundColor White
    Write-Host "  - MinIO Console: http://localhost:9001" -ForegroundColor White
    Write-Host "  - PostgreSQL: localhost:5432" -ForegroundColor White
    Write-Host ""
    Write-Host "برای مشاهده لاگ‌ها دستور زیر را بزنید:" -ForegroundColor Yellow
    Write-Host "  docker-compose logs -f" -ForegroundColor Gray
    Write-Host ""
    Write-Host "برای توقف سامانه:" -ForegroundColor Yellow
    Write-Host "  docker-compose down" -ForegroundColor Gray
    Write-Host "==========================================" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[خطا] در راه‌اندازی خطایی رخ داد. لاگ‌ها را بررسی کنید." -ForegroundColor Red
}

Read-Host "Press Enter to exit"
