from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """کاربر سفارشی با فیلدهای اضافی"""
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username or self.phone or str(self.id)
