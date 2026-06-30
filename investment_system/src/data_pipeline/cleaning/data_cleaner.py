"""
سیستم پاکسازی و اعتبارسنجی داده‌ها

قابلیت‌ها:
- حذف داده‌های پرت (IQR, Z-Score)
- مدیریت داده‌های گمشده
- نرمال‌سازی
- یکپارچه‌سازی فرمت‌ها
- تولید گزارش کیفیت داده
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    کلاس پاکسازی داده‌های مالی
    
    این کلاس متدهای مختلفی برای پاکسازی و آماده‌سازی داده‌ها ارائه می‌دهد
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        مقداردهی اولیه پاکسازی داده
        
        Args:
            config: پیکربندی پاکسازی
        """
        self.config = config or {
            'outlier_method': 'iqr',  # iqr, zscore
            'outlier_threshold': 1.5,
            'missing_method': 'median',  # mean, median, mode, interpolate
            'normalize_method': 'minmax',  # minmax, standard, robust
        }
        
        logger.info("پاکسازی داده مقداردهی شد")
    
    def remove_outliers_iqr(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        threshold: float = 1.5,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        حذف داده‌های پرت با روش IQR
        
        Args:
            df: دیتافریم ورودی
            columns: ستون‌های مورد بررسی (اختیاری)
            threshold: ضریب آستانه (معمولاً ۱.۵ یا ۳)
            
        Returns:
            دیتافریم پاکسازی شده و داده‌های حذف شده
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        mask = pd.Series(True, index=df.index)
        outliers_mask = pd.Series(False, index=df.index)
        
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            col_mask = (df[col] >= lower_bound) & (df[col] <= upper_bound)
            col_outliers = ~col_mask
            
            mask &= col_mask
            outliers_mask |= col_outliers
        
        cleaned_df = df[mask].copy()
        outliers_df = df[outliers_mask].copy()
        
        logger.info(f"تعداد {len(outliers_df)} داده پرت حذف شد ({len(outliers_df)/len(df)*100:.2f}%)")
        
        return cleaned_df, outliers_df
    
    def remove_outliers_zscore(
        self,
        df: pd.DataFrame,
        columns: Optional[List[str]] = None,
        threshold: float = 3.0,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        حذف داده‌های پرت با روش Z-Score
        
        Args:
            df: دیتافریم ورودی
            columns: ستون‌های مورد بررسی
            threshold: آستانه Z-Score (معمولاً ۳)
            
        Returns:
            دیتافریم پاکسازی شده و داده‌های حذف شده
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        z_scores = np.abs(stats.zscore(df[columns], nan_policy='omit'))
        mask = np.all(z_scores < threshold, axis=1)
        
        cleaned_df = df[mask].copy()
        outliers_df = df[~mask].copy()
        
        logger.info(f"تعداد {len(outliers_df)} داده پرت حذف شد با Z-Score")
        
        return cleaned_df, outliers_df
    
    def handle_missing_values(
        self,
        df: pd.DataFrame,
        method: str = 'median',
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        مدیریت داده‌های گمشده
        
        Args:
            df: دیتافریم ورودی
            method: روش پر کردن (mean, median, mode, interpolate, forward_fill, backward_fill)
            columns: ستون‌های مورد بررسی
            
        Returns:
            دیتافریم با داده‌های گمشده پر شده
        """
        if columns is None:
            columns = df.columns.tolist()
        
        df_cleaned = df.copy()
        
        for col in columns:
            if df_cleaned[col].isnull().sum() == 0:
                continue
            
            if method == 'mean':
                df_cleaned[col].fillna(df_cleaned[col].mean(), inplace=True)
            
            elif method == 'median':
                df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
            
            elif method == 'mode':
                df_cleaned[col].fillna(df_cleaned[col].mode()[0], inplace=True)
            
            elif method == 'interpolate':
                df_cleaned[col].interpolate(method='linear', inplace=True)
            
            elif method == 'forward_fill':
                df_cleaned[col].fillna(method='ffill', inplace=True)
            
            elif method == 'backward_fill':
                df_cleaned[col].fillna(method='bfill', inplace=True)
            
            elif method == 'drop':
                df_cleaned.dropna(subset=[col], inplace=True)
        
        missing_count = df_cleaned.isnull().sum().sum()
        logger.info(f"داده‌های گمشده مدیریت شدند. باقیمانده: {missing_count}")
        
        return df_cleaned
    
    def normalize(
        self,
        df: pd.DataFrame,
        method: str = 'minmax',
        columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        نرمال‌سازی داده‌ها
        
        Args:
            df: دیتافریم ورودی
            method: روش نرمال‌سازی (minmax, standard, robust, log)
            columns: ستون‌های مورد نرمال‌سازی
            
        Returns:
            دیتافریم نرمال‌شده
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        df_normalized = df.copy()
        
        for col in columns:
            if method == 'minmax':
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val - min_val > 0:
                    df_normalized[col] = (df[col] - min_val) / (max_val - min_val)
                else:
                    df_normalized[col] = 0
            
            elif method == 'standard':
                mean = df[col].mean()
                std = df[col].std()
                if std > 0:
                    df_normalized[col] = (df[col] - mean) / std
                else:
                    df_normalized[col] = 0
            
            elif method == 'robust':
                median = df[col].median()
                iqr = df[col].quantile(0.75) - df[col].quantile(0.25)
                if iqr > 0:
                    df_normalized[col] = (df[col] - median) / iqr
                else:
                    df_normalized[col] = 0
            
            elif method == 'log':
                # جلوگیری از لگاریتم اعداد منفی یا صفر
                df_normalized[col] = np.log1p(df[col].clip(lower=0))
        
        logger.info(f"نرمال‌سازی با روش {method} انجام شد")
        
        return df_normalized
    
    def standardize_formats(
        self,
        df: pd.DataFrame,
        date_columns: Optional[List[str]] = None,
        numeric_columns: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        یکپارچه‌سازی فرمت داده‌ها
        
        Args:
            df: دیتافریم ورودی
            date_columns: ستون‌های تاریخ
            numeric_columns: ستون‌های عددی
            
        Returns:
            دیتافریم با فرمت استاندارد
        """
        df_standardized = df.copy()
        
        # استانداردسازی تاریخ
        if date_columns:
            for col in date_columns:
                try:
                    df_standardized[col] = pd.to_datetime(df_standardized[col])
                except Exception as e:
                    logger.warning(f"خطا در تبدیل تاریخ ستون {col}: {e}")
        
        # استانداردسازی اعداد (حذف کاما، تبدیل به عدد)
        if numeric_columns:
            for col in numeric_columns:
                try:
                    # تبدیل به رشته و حذف کاراکترهای غیرعددی
                    df_standardized[col] = df_standardized[col].astype(str).str.replace(',', '')
                    df_standardized[col] = pd.to_numeric(df_standardized[col], errors='coerce')
                except Exception as e:
                    logger.warning(f"خطا در تبدیل عددی ستون {col}: {e}")
        
        logger.info("فرمت داده‌ها استاندارد شد")
        
        return df_standardized
    
    def generate_quality_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        تولید گزارش کیفیت داده
        
        Args:
            df: دیتافریم مورد بررسی
            
        Returns:
            گزارش کیفیت داده
        """
        report = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
            'missing_values': {},
            'duplicate_rows': df.duplicated().sum(),
            'data_types': df.dtypes.to_dict(),
            'numeric_stats': {},
            'categorical_stats': {},
        }
        
        # داده‌های گمشده
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_percent = (missing_count / len(df)) * 100
            if missing_count > 0:
                report['missing_values'][col] = {
                    'count': missing_count,
                    'percent': round(missing_percent, 2),
                }
        
        # آمار ستون‌های عددی
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            report['numeric_stats'][col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'median': df[col].median(),
                'skewness': df[col].skew(),
                'kurtosis': df[col].kurtosis(),
            }
        
        # آمار ستون‌های دسته‌ای
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            report['categorical_stats'][col] = {
                'unique_count': df[col].nunique(),
                'most_common': df[col].value_counts().head(5).to_dict(),
            }
        
        logger.info("گزارش کیفیت داده تولید شد")
        
        return report
    
    def clean(
        self,
        df: pd.DataFrame,
        remove_outliers: bool = True,
        handle_missing: bool = True,
        normalize: bool = False,
    ) -> pd.DataFrame:
        """
        اجرای کامل خط لوله پاکسازی
        
        Args:
            df: دیتافریم ورودی
            remove_outliers: حذف داده‌های پرت
            handle_missing: مدیریت داده‌های گمشده
            normalize: نرمال‌سازی
            
        Returns:
            دیتافریم پاکسازی شده
        """
        logger.info("شروع خط لوله پاکسازی داده")
        
        # حذف داده‌های پرت
        if remove_outliers:
            df, outliers = self.remove_outliers_iqr(df)
        
        # مدیریت داده‌های گمشده
        if handle_missing:
            df = self.handle_missing_values(df, method=self.config['missing_method'])
        
        # نرمال‌سازی
        if normalize:
            df = self.normalize(df, method=self.config['normalize_method'])
        
        logger.info("خط لوله پاکسازی تکمیل شد")
        
        return df
