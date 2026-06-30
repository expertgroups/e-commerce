"""
خزنده بورس تهران برای دریافت داده‌های قیمت و معاملات

قابلیت‌ها:
- دریافت داده‌های OHLCV روزانه با pytse-client
- دریافت اطلاعات نمادها
- تعدیل قیمت‌ها (افزایش سرمایه، سود)
- مدیریت تاریخ شمسی
- دریافت داده‌های تاریخی (۵ سال)
- Cache کردن داده‌ها
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class TSECrawler(BaseCrawler):
    """
    خزنده بورس تهران
    
    استفاده از کتابخانه pytse-client برای دریافت داده‌ها
    """
    
    def __init__(
        self,
        base_url: str = "https://www.tsetmc.com",
        timeout: int = 30,
        retry_count: int = 3,
        use_pytse: bool = True,
        **kwargs: Any,
    ) -> None:
        """
        مقداردهی اولیه خزنده بورس
        
        Args:
            base_url: آدرس پایه بورس
            timeout: زمان انتظار
            retry_count: تعداد تلاش مجدد
            use_pytse: استفاده از pytse-client
        """
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            retry_count=retry_count,
            rate_limit_delay=1.0,
            **kwargs,
        )
        
        self.use_pytse = use_pytse
        self.symbols_cache: Optional[Dict[str, Any]] = None
    
    def get_symbols_list(self) -> List[Dict[str, Any]]:
        """
        دریافت لیست تمام نمادهای فعال
        
        Returns:
            لیست نمادها با اطلاعات کامل
        """
        if self.symbols_cache is not None:
            return list(self.symbols_cache.values())
        
        try:
            if self.use_pytse:
                import tse
                symbols_info = tse.all_symbols()
                
                self.symbols_cache = {}
                for row in symbols_info:
                    symbol = row[0]
                    self.symbols_cache[symbol] = {
                        'symbol': symbol,
                        'name': row[1],
                        'industry': row[2] if len(row) > 2 else None,
                        'market': row[3] if len(row) > 3 else None,
                    }
                
                logger.info(f"تعداد {len(self.symbols_cache)} نماد بارگذاری شد")
                return list(self.symbols_cache.values())
            
        except Exception as e:
            logger.error(f"خطا در دریافت لیست نمادها: {e}")
        
        return []
    
    def get_daily_price(
        self,
        symbol: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        adjusted: bool = True,
    ) -> Optional[pd.DataFrame]:
        """
        دریافت داده‌های قیمت روزانه
        
        Args:
            symbol: نماد شرکت
            start_date: تاریخ شروع (اختیاری)
            end_date: تاریخ پایان (اختیاری)
            adjusted: اعمال تعدیل قیمت
            
        Returns:
            دیتافریم داده‌های OHLCV
        """
        cache_key = f"{symbol}_{start_date}_{end_date}_{adjusted}"
        cached_data = self._load_from_cache(cache_key)
        
        if cached_data is not None:
            df = pd.DataFrame(cached_data)
            df['date'] = pd.to_datetime(df['date'])
            return df
        
        try:
            if self.use_pytse:
                import tse
                
                # دریافت داده‌ها
                df = tse.get_price_history(symbol=symbol, adjust=adjusted)
                
                if df is not None and not df.empty:
                    # فیلتر بر اساس تاریخ
                    if start_date:
                        df = df[df.index >= start_date]
                    if end_date:
                        df = df[df.index <= end_date]
                    
                    # استانداردسازی نام ستون‌ها
                    df = df.reset_index()
                    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 
                                  'value', 'last', 'first', 'count']
                    
                    # ذخیره در کش
                    self._save_to_cache(cache_key, df.to_dict('records'))
                    
                    logger.info(f"داده‌های {symbol} بارگذاری شد: {len(df)} رکورد")
                    return df
            
        except Exception as e:
            logger.error(f"خطا در دریافت قیمت {symbol}: {e}")
        
        return None
    
    def get_historical_data(
        self,
        symbol: str,
        days: int = 1825,  # 5 years
    ) -> Optional[pd.DataFrame]:
        """
        دریافت داده‌های تاریخی
        
        Args:
            symbol: نماد شرکت
            days: تعداد روزهای گذشته
            
        Returns:
            دیتافریم داده‌های تاریخی
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return self.get_daily_price(
            symbol=symbol,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
        )
    
    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        دریافت اطلاعات کامل یک نماد
        
        Args:
            symbol: نماد شرکت
            
        Returns:
            اطلاعات نماد
        """
        try:
            if self.use_pytse:
                import tse
                
                ticker = tse.Ticker(symbol)
                
                info = {
                    'symbol': symbol,
                    'name': ticker.title,
                    'industry': ticker.group_name,
                    'market_cap': ticker.market_cap,
                    'shares_base': ticker.base_volume,
                    'eps': ticker.eps,
                    'pe': ticker.pe,
                    'nav': ticker.nav if hasattr(ticker, 'nav') else None,
                }
                
                return info
                
        except Exception as e:
            logger.error(f"خطا در دریافت اطلاعات {symbol}: {e}")
        
        return None
    
    def get_trade_details(self, symbol: str, date: str) -> Optional[Dict[str, Any]]:
        """
        دریافت جزئیات معاملات یک روز
        
        Args:
            symbol: نماد شرکت
            date: تاریخ مورد نظر
            
        Returns:
            جزئیات معاملات
        """
        try:
            if self.use_pytse:
                import tse
                
                ticker = tse.Ticker(symbol)
                
                # دریافت داده‌های حقیقی/حقوقی
                buyer_individual = ticker.buy_quantity_individual
                seller_individual = ticker.sell_quantity_individual
                buyer_legal = ticker.buy_quantity_legal
                seller_legal = ticker.sell_quantity_legal
                
                return {
                    'symbol': symbol,
                    'date': date,
                    'buyer_individual': buyer_individual,
                    'seller_individual': seller_individual,
                    'buyer_legal': buyer_legal,
                    'seller_legal': seller_legal,
                    'power_ratio': (buyer_individual / seller_individual) if seller_individual > 0 else None,
                }
                
        except Exception as e:
            logger.error(f"خطا در دریافت جزئیات معاملات {symbol}: {e}")
        
        return None
    
    def get_market_index(self) -> Optional[pd.DataFrame]:
        """
        دریافت شاخص کل بازار
        
        Returns:
            دیتافریم شاخص کل
        """
        try:
            if self.use_pytse:
                import finpy_tse as fts
                
                # دریافت شاخص کل
                index_data = fts.GetMarketDailyData()
                
                if index_data is not None:
                    df = pd.DataFrame(index_data)
                    logger.info(f"شاخص کل بارگذاری شد: {len(df)} رکورد")
                    return df
                    
        except Exception as e:
            logger.error(f"خطا در دریافت شاخص کل: {e}")
        
        return None
    
    def get_sector_index(self, sector_code: str) -> Optional[pd.DataFrame]:
        """
        دریافت شاخص صنعت
        
        Args:
            sector_code: کد صنعت
            
        Returns:
            دیتافریم شاخص صنعت
        """
        try:
            if self.use_pytse:
                import finpy_tse as fts
                
                sector_data = fts.GetSectorDailyData(sector_code)
                
                if sector_data is not None:
                    df = pd.DataFrame(sector_data)
                    logger.info(f"شاخص صنعت {sector_code} بارگذاری شد")
                    return df
                    
        except Exception as e:
            logger.error(f"خطا در دریافت شاخص صنعت {sector_code}: {e}")
        
        return None
    
    def run(
        self,
        symbols: Optional[List[str]] = None,
        days: int = 1825,
        save_dir: Path = Path("./data/tse"),
    ) -> Dict[str, Any]:
        """
        اجرای اصلی خزنده بورس
        
        Args:
            symbols: لیست نمادها (اختیاری)
            days: تعداد روزهای تاریخی
            save_dir: مسیر ذخیره‌سازی
            
        Returns:
            داده‌های استخراج شده
        """
        logger.info("شروع اجرای خزنده بورس")
        
        if symbols is None:
            symbols_info = self.get_symbols_list()
            symbols = [s['symbol'] for s in symbols_info[:50]]  # محدود به ۵۰ نماد برای تست
        
        results = {
            'symbols': [],
            'prices': {},
            'info': {},
        }
        
        save_dir.mkdir(parents=True, exist_ok=True)
        
        for symbol in symbols:
            logger.info(f"پردازش نماد {symbol}")
            
            try:
                # دریافت داده‌های قیمت
                prices = self.get_historical_data(symbol, days)
                
                if prices is not None:
                    # ذخیره در فایل CSV
                    prices_file = save_dir / f"{symbol}_prices.csv"
                    prices.to_csv(prices_file, index=False)
                    results['prices'][symbol] = str(prices_file)
                
                # دریافت اطلاعات نماد
                info = self.get_symbol_info(symbol)
                if info:
                    results['info'][symbol] = info
                
                results['symbols'].append(symbol)
                
            except Exception as e:
                logger.error(f"خطا در پردازش {symbol}: {e}")
                continue
        
        logger.info(f"خزنده بورس با موفقیت اجرا شد. {len(results['symbols'])} نماد پردازش شد")
        return results
    
    def close(self) -> None:
        """پاکسازی منابع"""
        self.symbols_cache = None
        super().close()
