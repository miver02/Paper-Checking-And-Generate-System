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
USERNAME_MAX_LENGTH = 30
EMAIL_MAX_LENGTH = 255
BIO_MAX_LENGTH = 500


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)

    phone = models.CharField(
        max_length=11, unique=True, validators=[RegexValidator(PHONE_REGEX)]
    )

    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)

    avatar = models.ImageField(
        upload_to=user_avatar_upload_path,
        blank=True,
        null=True,
        default="static/avatars/default.png",
    )

    bio = models.TextField(max_length=500, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
