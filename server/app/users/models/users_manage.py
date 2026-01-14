from django.contrib.auth.base_user import BaseUserManager
import os

# 优化头像上传路径：动态分目录，避免单目录文件过多
def user_avatar_upload_path(instance, filename):
    """
    用户头像上传路径生成函数
    :param instance: User实例
    :param filename: 原始文件名
    :return: 拼接后的上传路径（如avatars/2025/05/12/1/avatar.png）
    """
    ext = os.path.splitext(filename)[1].lower()
    return f"avatars/{instance.pk}/avatar{ext}"


class CustomUserManager(BaseUserManager):
    """自定义用户管理器"""

    # ========= 内部工具方法 =========

    @staticmethod
    def _normalize_phone(phone: str) -> str:
        """统一手机号格式（去空格、横线）"""
        if not phone:
            raise ValueError("手机号不能为空")
        return phone.strip().replace("-", "").replace(" ", "")

    def _create_user(self, phone: str, password: str | None = None, **extra_fields):
        """
        创建用户的底层实现（统一入口）
        """
        phone = self._normalize_phone(phone)

        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        # 🔥 主动触发 Model 层校验（字段长度 / unique / clean）
        user.full_clean()
        user.save(using=self._db)
        return user

    # ========= 对外 API =========

    def create_user(self, phone: str, password: str | None = None, **extra_fields):
        """创建普通用户"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone: str, password: str | None = None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("超级用户必须 is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("超级用户必须 is_superuser=True")

        return self._create_user(phone, password, **extra_fields)


