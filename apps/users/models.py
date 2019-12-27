from django.db import models
from django.contrib.auth.models import AbstractUser, User  # 引入默认user字段


# Create your models here.
class UserProfile(AbstractUser):
    """
    用户表
    """
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
