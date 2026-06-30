"""
کلاس پایه برای تمام خزنده‌های داده

این کلاس امکانات مشترک برای خزنده‌های مختلف را فراهم می‌کند:
- مدیریت درخواست‌های HTTP با retry و timeout
- پردازش پاسخ‌ها (JSON, HTML, PDF, Excel)
- ذخیره‌سازی داده‌های خام
- مدیریت خطا و لاگ‌گیری
- Rate Limiting
- Cache Management
"""

import logging
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class BaseCrawler(ABC):
    """
    کلاس پایه برای خزنده‌ها
    
    Attributes:
        base_url (str): آدرس پایه API یا وبسایت
        session (requests.Session): نشست HTTP با تنظیمات بهینه
        cache_dir (Path): مسیر ذخیره‌سازی کش
        rate_limit_delay (float): تأخیر بین درخواست‌ها
    """
    
    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        retry_count: int = 3,
        rate_limit_delay: float = 1.0,
        cache_enabled: bool = True,
        cache_dir: Optional[Path] = None,
    ) -> None:
        """
        مقداردهی اولیه خزنده
        
        Args:
            base_url: آدرس پایه
            timeout: زمان انتظار حداکثر برای درخواست‌ها
            retry_count: تعداد تلاش مجدد در صورت شکست
            rate_limit_delay: تأخیر بین درخواست‌ها بر حسب ثانیه
            cache_enabled: فعال‌سازی کش
            cache_dir: مسیر پوشه کش
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.rate_limit_delay = rate_limit_delay
        self.cache_enabled = cache_enabled
        self.cache_dir = cache_dir or Path("./data/cache")
        
        if cache_enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # تنظیمات retry برای مدیریت خطاهای شبکه
        retry_strategy = Retry(
            total=retry_count,
            backoff_factor=1.0,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session = requests.Session()
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # هدرهای پیش‌فرض
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/html, */*",
            "Accept-Language": "fa-IR,fa;q=0.9,en-US;q=0.8",
        })
        
        logger.info(f"خزنده {self.__class__.__name__} مقداردهی شد")
    
    def _rate_limit(self) -> None:
        """اعمال محدودیت نرخ درخواست‌ها"""
        if self.rate_limit_delay > 0:
            time.sleep(self.rate_limit_delay)
    
    def _get_cache_path(self, key: str) -> Path:
        """
        تولید مسیر فایل کش
        
        Args:
            key: کلید منحصر به فرد برای داده
            
        Returns:
            مسیر کامل فایل کش
        """
        safe_key = "".join(c for c in key if c.isalnum() or c in "-_")
        return self.cache_dir / f"{safe_key}.json"
    
    def _load_from_cache(self, key: str) -> Optional[Any]:
        """
        بارگذاری داده از کش
        
        Args:
            key: کلید داده
            
        Returns:
            داده کش شده یا None
        """
        if not self.cache_enabled:
            return None
        
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                import json
                with open(cache_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.debug(f"داده از کش بارگذاری شد: {key}")
                return data
            except Exception as e:
                logger.warning(f"خطا در بارگذاری کش {key}: {e}")
        return None
    
    def _save_to_cache(self, key: str, data: Any) -> None:
        """
        ذخیره داده در کش
        
        Args:
            key: کلید داده
            data: داده برای ذخیره
        """
        if not self.cache_enabled:
            return
        
        try:
            import json
            cache_path = self._get_cache_path(key)
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug(f"داده در کش ذخیره شد: {key}")
        except Exception as e:
            logger.error(f"خطا در ذخیره کش {key}: {e}")
    
    def fetch_json(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        use_cache: bool = True,
    ) -> Optional[Union[Dict, List]]:
        """
        دریافت داده JSON از API
        
        Args:
            endpoint: اندپوینت API
            params: پارامترهای درخواست
            use_cache: استفاده از کش
            
        Returns:
            داده JSON یا None در صورت شکست
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        cache_key = f"{endpoint}_{str(params)}" if params else endpoint
        
        # بررسی کش
        if use_cache:
            cached_data = self._load_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
        
        # اعمال rate limiting
        self._rate_limit()
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            # ذخیره در کش
            if use_cache:
                self._save_to_cache(cache_key, data)
            
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout در درخواست به {url}")
        except requests.exceptions.RequestException as e:
            logger.error(f"خطا در درخواست به {url}: {e}")
        except ValueError as e:
            logger.error(f"خطا در پردازش JSON: {e}")
        
        return None
    
    def fetch_html(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        دریافت صفحه HTML
        
        Args:
            endpoint: آدرس صفحه
            params: پارامترهای درخواست
            
        Returns:
            محتوای HTML یا None
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        self._rate_limit()
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطا در دریافت HTML از {url}: {e}")
            return None
    
    def fetch_pdf(
        self,
        url: str,
        save_path: Path,
    ) -> Optional[Path]:
        """
        دانلود فایل PDF
        
        Args:
            url: آدرس فایل PDF
            save_path: مسیر ذخیره‌سازی
            
        Returns:
            مسیر فایل ذخیره شده یا None
        """
        self._rate_limit()
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"PDF دانلود شد: {save_path}")
            return save_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطا در دانلود PDF: {e}")
            return None
    
    def fetch_excel(
        self,
        url: str,
        save_path: Path,
    ) -> Optional[Path]:
        """
        دانلود فایل Excel
        
        Args:
            url: آدرس فایل Excel
            save_path: مسیر ذخیره‌سازی
            
        Returns:
            مسیر فایل ذخیره شده یا None
        """
        self._rate_limit()
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Excel دانلود شد: {save_path}")
            return save_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"خطا در دانلود Excel: {e}")
            return None
    
    @abstractmethod
    def run(self, **kwargs: Any) -> Any:
        """
        اجرای اصلی خزنده
        
        این متد باید در کلاس‌های فرزند پیاده‌سازی شود
        
        Args:
            **kwargs: پارامترهای اختصاصی هر خزنده
            
        Returns:
            داده‌های استخراج شده
        """
        pass
    
    def close(self) -> None:
        """بستن نشست HTTP"""
        self.session.close()
        logger.info("نشست HTTP بسته شد")
    
    def __enter__(self) -> 'BaseCrawler':
        """ورود به context manager"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """خروج از context manager"""
        self.close()
