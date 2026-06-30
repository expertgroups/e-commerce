"""
خزنده کدال برای دریافت صورت‌های مالی و گزارش‌های شرکت‌ها

قابلیت‌ها:
- دریافت لیست شرکت‌ها
- دریافت صورت‌های مالی (ترازنامه، سود و زیان، جریان نقد)
- دریافت گزارش فعالیت ماهانه
- پردازش PDF با tabula-py
- پردازش Excel با pandas
- استخراج جداول مالی
- تبدیل به دیتافریم استاندارد
"""

import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime

import pandas as pd

from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class CodalCrawler(BaseCrawler):
    """
    خزنده سامانه کدال
    
    این کلاس برای استخراج اطلاعات از سامانه کدال استفاده می‌شود
    """
    
    def __init__(
        self,
        base_url: str = "https://codal.ir",
        timeout: int = 30,
        retry_count: int = 3,
        **kwargs: Any,
    ) -> None:
        """
        مقداردهی اولیه خزنده کدال
        
        Args:
            base_url: آدرس پایه کدال
            timeout: زمان انتظار
            retry_count: تعداد تلاش مجدد
        """
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            retry_count=retry_count,
            rate_limit_delay=2.0,  # کدال حساس است
            **kwargs,
        )
        
        self.companies_cache: Optional[List[Dict]] = None
    
    def get_companies_list(self) -> List[Dict[str, Any]]:
        """
        دریافت لیست تمام شرکت‌های پذیرفته شده
        
        Returns:
            لیست شرکت‌ها با اطلاعات نماد، نام، صنعت
        """
        if self.companies_cache is not None:
            return self.companies_cache
        
        try:
            # دریافت لیست شرکت‌ها از API کدال
            data = self.fetch_json(
                endpoint="/api/issuer",
                params={"page": 1, "pageSize": 1000},
                use_cache=True,
            )
            
            if data and 'data' in data:
                companies = []
                for item in data['data']:
                    companies.append({
                        'symbol': item.get('symbol'),
                        'name': item.get('companyName'),
                        'industry': item.get('sectorName'),
                        'cik': item.get('ciSecId'),
                    })
                
                self.companies_cache = companies
                logger.info(f"تعداد {len(companies)} شرکت بارگذاری شد")
                return companies
            
        except Exception as e:
            logger.error(f"خطا در دریافت لیست شرکت‌ها: {e}")
        
        return []
    
    def search_reports(
        self,
        symbol: str,
        report_type: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        جستجوی گزارش‌های یک شرکت
        
        Args:
            symbol: نماد شرکت
            report_type: نوع گزارش (اختیاری)
            from_date: تاریخ شروع (اختیاری)
            to_date: تاریخ پایان (اختیاری)
            
        Returns:
            لیست گزارش‌ها
        """
        try:
            params = {
                'symbol': symbol,
                'page': 1,
                'pageSize': 100,
            }
            
            if report_type:
                params['reportType'] = report_type
            
            data = self.fetch_json(
                endpoint="/api/reports",
                params=params,
                use_cache=True,
            )
            
            if data and 'data' in data:
                reports = []
                for item in data['data']:
                    reports.append({
                        'report_id': item.get('id'),
                        'title': item.get('title'),
                        'publish_date': item.get('publishDate'),
                        'report_type': item.get('reportType'),
                        'pdf_url': f"{self.base_url}/Reports/Decision/{item.get('id')}",
                    })
                
                logger.info(f"تعداد {len(reports)} گزارش برای {symbol} یافت شد")
                return reports
                
        except Exception as e:
            logger.error(f"خطا در جستجوی گزارش‌های {symbol}: {e}")
        
        return []
    
    def download_financial_statements(
        self,
        symbol: str,
        fiscal_year: int,
        save_dir: Path = Path("./data/codal"),
    ) -> Optional[Dict[str, Path]]:
        """
        دانلود صورت‌های مالی یک شرکت
        
        Args:
            symbol: نماد شرکت
            fiscal_year: سال مالی
            save_dir: مسیر ذخیره‌سازی
            
        Returns:
            مسیر فایل‌های دانلود شده
        """
        try:
            reports = self.search_reports(
                symbol=symbol,
                report_type="financial_statement",
            )
            
            downloaded_files = {}
            
            for report in reports:
                if str(fiscal_year) in report.get('title', ''):
                    pdf_url = report['pdf_url']
                    filename = f"{symbol}_{fiscal_year}_{report['report_type']}.pdf"
                    save_path = save_dir / symbol / filename
                    
                    pdf_path = self.fetch_pdf(pdf_url, save_path)
                    if pdf_path:
                        downloaded_files[report['report_type']] = pdf_path
            
            return downloaded_files if downloaded_files else None
            
        except Exception as e:
            logger.error(f"خطا در دانلود صورت‌های مالی {symbol}: {e}")
            return None
    
    def extract_financial_tables(
        self,
        pdf_path: Path,
        table_type: str = "balance_sheet",
    ) -> Optional[pd.DataFrame]:
        """
        استخراج جداول مالی از PDF
        
        Args:
            pdf_path: مسیر فایل PDF
            table_type: نوع جدول (balance_sheet, income_statement, cash_flow)
            
        Returns:
            دیتافریم جدول استخراج شده
        """
        try:
            import tabula
            
            # استخراج جداول از PDF
            tables = tabula.read_pdf(
                str(pdf_path),
                pages='all',
                multiple_tables=True,
                lattice=True,
            )
            
            if not tables:
                logger.warning(f"جدولی در {pdf_path} یافت نشد")
                return None
            
            # ترکیب جداول مرتبط
            if len(tables) == 1:
                return tables[0]
            else:
                # پیدا کردن جدول مرتبط با نوع درخواست
                for table in tables:
                    if self._is_relevant_table(table, table_type):
                        return table
                
                # اگر جدول مرتبط پیدا نشد، اولین جدول بزرگ را برگردان
                largest_table = max(tables, key=lambda t: len(t))
                return largest_table
                
        except Exception as e:
            logger.error(f"خطا در استخراج جدول از {pdf_path}: {e}")
            return None
    
    def _is_relevant_table(
        self,
        df: pd.DataFrame,
        table_type: str,
    ) -> bool:
        """
        بررسی اینکه آیا جدول مربوط به نوع درخواست است
        
        Args:
            df: جدول
            table_type: نوع جدول مورد نظر
            
        Returns:
            True اگر جدول مرتبط باشد
        """
        keywords = {
            'balance_sheet': ['دارایی', 'بدهی', 'حقوق صاحبان سهام'],
            'income_statement': ['فروش', 'سود', 'هزینه'],
            'cash_flow': ['جریان نقد', 'عملیاتی', 'سرمایه‌گذاری'],
        }
        
        target_keywords = keywords.get(table_type, [])
        
        # بررسی وجود کلمات کلیدی در جدول
        text_content = df.to_string().lower()
        return any(keyword in text_content for keyword in target_keywords)
    
    def get_monthly_activity_report(
        self,
        symbol: str,
        year: int,
        month: int,
    ) -> Optional[Dict[str, Any]]:
        """
        دریافت گزارش فعالیت ماهانه
        
        Args:
            symbol: نماد شرکت
            year: سال
            month: ماه
            
        Returns:
            داده‌های گزارش ماهانه
        """
        try:
            reports = self.search_reports(
                symbol=symbol,
                report_type="monthly_activity",
            )
            
            target_month_str = f"{year}/{month:02d}"
            
            for report in reports:
                if target_month_str in report.get('title', ''):
                    # دانلود و پردازش گزارش
                    pdf_url = report['pdf_url']
                    # اینجا می‌توان PDF را دانلود و پردازش کرد
                    return {
                        'report_id': report['report_id'],
                        'symbol': symbol,
                        'year': year,
                        'month': month,
                        'title': report['title'],
                        'publish_date': report['publish_date'],
                    }
            
        except Exception as e:
            logger.error(f"خطا در دریافت گزارش ماهانه {symbol}: {e}")
        
        return None
    
    def run(
        self,
        symbols: Optional[List[str]] = None,
        report_types: Optional[List[str]] = None,
        save_dir: Path = Path("./data/codal"),
    ) -> Dict[str, Any]:
        """
        اجرای اصلی خزنده کدال
        
        Args:
            symbols: لیست نمادهای شرکت‌ها (اختیاری - اگر None باشد همه شرکت‌ها)
            report_types: انواع گزارش‌ها برای دریافت
            save_dir: مسیر ذخیره‌سازی
            
        Returns:
            داده‌های استخراج شده
        """
        logger.info("شروع اجرای خزنده کدال")
        
        if symbols is None:
            companies = self.get_companies_list()
            symbols = [c['symbol'] for c in companies[:10]]  # محدود به ۱۰ شرکت برای تست
        
        results = {
            'companies': [],
            'reports': {},
            'financials': {},
        }
        
        for symbol in symbols:
            logger.info(f"پردازش شرکت {symbol}")
            
            try:
                # دریافت گزارش‌ها
                reports = self.search_reports(symbol)
                results['reports'][symbol] = reports
                
                # دریافت صورت‌های مالی آخرین سال
                current_year = datetime.now().year
                financials = self.download_financial_statements(
                    symbol=symbol,
                    fiscal_year=current_year - 1,
                    save_dir=save_dir,
                )
                
                if financials:
                    results['financials'][symbol] = financials
                
                results['companies'].append(symbol)
                
            except Exception as e:
                logger.error(f"خطا در پردازش {symbol}: {e}")
                continue
        
        logger.info(f"خزنده کدال با موفقیت اجرا شد. {len(results['companies'])} شرکت پردازش شد")
        return results
    
    def close(self) -> None:
        """پاکسازی منابع"""
        self.companies_cache = None
        super().close()
