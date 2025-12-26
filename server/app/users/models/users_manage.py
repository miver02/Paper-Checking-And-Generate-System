from django.contrib.auth.base_user import BaseUserManager
import os
from django.utils import timezone


# 优化头像上传路径：动态分目录，避免单目录文件过多
def user_avatar_upload_path(instance, filename):
    """
    用户头像上传路径生成函数
    :param instance: User实例
    :param filename: 原始文件名
    :return: 拼接后的上传路径（如avatars/2025/05/12/1/avatar.png）
    """
    # 新增用户（无ID）时临时存储
    if not instance.pk:
        return f"avatars/temp/{os.path.basename(filename)}"
    # 已有用户：按日期+用户ID分目录
    date_str = timezone.now().strftime("%Y/%m/%d")
    return f"avatars/{date_str}/{instance.pk}/{os.path.basename(filename)}"


class CustomUserManager(BaseUserManager):
    """自定义用户管理器"""

    def _create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("手机号不能为空")

        phone = phone.strip().replace("-", "").replace(" ", "")

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.full_clean()  # 🔥 关键：触发 Model 校验
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(phone, password, **extra_fields)


    def update_user_fields(self, user_id: int, **fields):
        """
        纯数据库层更新，不做业务判断
        """
        if not fields:
            return 0

        # 防止非法字段写入
        allowed_fields = {
            "username",
            "email",
            "avatar",
            "bio",
            "is_active",
        }

        update_data = {
            k: v for k, v in fields.items()
            if k in allowed_fields
        }

        if not update_data:
            return 0

        return self.filter(id=user_id).update(**update_data)

        
    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields["is_staff"]:
            raise ValueError("超级用户必须 is_staff=True")
        if not extra_fields["is_superuser"]:
            raise ValueError("超级用户必须 is_superuser=True")

        return self._create_user(phone, password, **extra_fields)
