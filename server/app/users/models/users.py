from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

# 导入模型
from .users_manage import CustomUserManager, user_avatar_upload_path

# 抽离常量：提升可维护性，避免硬编码
PHONE_REGEX = r"^1[3-9]\d{9}$"


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30, unique=True, null=True, blank=True, editable=False)

    phone = models.CharField(
        max_length=11, unique=True, validators=[RegexValidator(PHONE_REGEX)]
    )

    email = models.EmailField(
        max_length=255, unique=True, null=True, blank=True)

    display_name = models.CharField(max_length=30, null=True, blank=True)

    avatar = models.ImageField(
        upload_to=user_avatar_upload_path,
        blank=True,
        null=True,
    )

    bio = models.TextField(max_length=500, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_phone_change_at = models.DateTimeField(null=True)

    objects = CustomUserManager()   # Django / auth / admin
    users = CustomUserManager()     # 业务层 API

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old = User.objects.get(pk=self.pk)
                if old.avatar and old.avatar != self.avatar:
                    old.avatar.delete(save=False)
            except User.DoesNotExist:
                pass

        super().save(*args, **kwargs)