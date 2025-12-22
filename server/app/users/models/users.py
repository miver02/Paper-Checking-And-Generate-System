import os
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.forms import ValidationError
from django.utils import timezone
from django.conf import settings

# 抽离常量：提升可维护性，避免硬编码
PHONE_REGEX = r"^1[3-9]\d{9}$"
USERNAME_MAX_LENGTH = 30
EMAIL_MAX_LENGTH = 255
BIO_MAX_LENGTH = 500

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
    """自定义用户管理器（支持普通用户、员工用户和超级用户创建）"""

    def create_user(self, phone, password=None, **extra_fields):
        """创建普通用户（核心逻辑，必需手机号）"""
        if not phone:
            raise ValueError("手机号是必填字段，不能为空")
        
        phone = phone.strip().replace("-", "").replace(" ", "")
        phone_validator = RegexValidator(PHONE_REGEX, message="请输入有效的11位手机号码")
        try:
            phone_validator(phone)
        except ValidationError:
            raise ValueError("请输入有效的11位手机号码")
        
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_deleted", False)
        extra_fields.setdefault("is_superuser", False)
        
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, password=None, **extra_fields):
        """创建具有后台管理权限但非超级用户的员工账户"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_deleted", False)
        extra_fields.setdefault("is_superuser", False)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("员工账户必须设置 is_staff=True.")
            
        return self.create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_deleted", False)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("超级用户必须设置 is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("超级用户必须设置 is_superuser=True.")
        
        return self.create_user(phone, password, **extra_fields)

    def delete_superuser(self, phone=None):
        """修复：使用self.model替代硬编码的User，提升兼容性"""
        try:
            user = self.model.objects.get(phone=phone)
            user.delete()
            print("用户删除成功！")
        except self.model.DoesNotExist:
            print("错误：该手机号对应的用户不存在！")
        except Exception as e:
            print(f"删除失败：{str(e)}")

    def get_queryset(self):
        """重写查询集：默认过滤软删除的用户"""
        return super().get_queryset().filter(is_deleted=False)


class User(AbstractBaseUser, PermissionsMixin):
    """
    自定义用户模型（支持超级用户权限）
    核心字段：手机号（登录认证）、用户名、邮箱、头像等基础信息
    """
    # 核心登录字段：用户名（可选，昵称）
    username = models.CharField(
        verbose_name="用户名",
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        blank=True,
        null=True,
        help_text="用户自定义昵称，唯一标识，最长30个字符"
    )

    # 核心认证字段：手机号（唯一，登录用）
    phone = models.CharField(
        verbose_name="手机号码",
        max_length=11,
        unique=True,
        validators=[RegexValidator(PHONE_REGEX, message="请输入有效的11位手机号码")],
        help_text="用于登录和接收验证码，格式为11位数字"
    )

    # 扩展字段：邮箱（可选）
    email = models.EmailField(
        verbose_name="邮箱",
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        blank=True,
        null=True,
        help_text="用于接收邮件通知，需符合邮箱格式"
    )

    # 扩展字段：头像（可选，默认头像）
    avatar = models.ImageField(
        verbose_name="头像",
        upload_to=user_avatar_upload_path,
        blank=True,
        null=True,
        # 修复：默认值使用静态文件路径（而非URL）
        default="static/avatars/default.png",
        help_text="用户头像图片，支持JPG/PNG格式，建议尺寸200x200"
    )

    # 扩展字段：个人简介（可选，限制长度）
    bio = models.TextField(
        verbose_name="个人简介",
        blank=True,
        null=True,
        max_length=BIO_MAX_LENGTH,
        help_text="个人简介，最长500个字符"
    )

    # 时间字段：命名规范，符合Django习惯
    created_at = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新时间", auto_now=True)

    # 软删除字段：标记删除，不物理删除数据
    is_deleted = models.BooleanField(
        verbose_name="是否软删除",
        default=False,
        help_text="标记用户是否删除（软删除，不物理删除数据）"
    )

    # 认证必需字段（无后台权限需求，仅保留基础激活状态）
    is_staff = models.BooleanField(
        verbose_name="是否后台管理员",
        default=False,
        help_text="用户可以登录到管理站点"
    )
    
    is_active = models.BooleanField(
        verbose_name="是否激活",
        default=True,
        help_text="是否允许用户登录（禁用账号时设为False）"
    )

    # 指定用户管理器
    objects = CustomUserManager()

    # 核心配置：指定手机号为登录认证字段（替代默认username）
    USERNAME_FIELD = "phone"
    # 无必需扩展字段（创建用户仅需手机号）
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        db_table = "users"
        app_label = "app_users"
        # 性能优化：添加核心索引
        indexes = [
            models.Index(fields=["phone"]),  # 登录查询核心索引
            models.Index(fields=["username"]),  # 按用户名查询索引
            models.Index(fields=["is_deleted", "is_active"]),  # 筛选有效用户
            models.Index(fields=["created_at"]),  # 按创建时间筛选
        ]
        # 默认排序：按创建时间倒序（最新创建在前）
        ordering = ["-created_at"]

    def __str__(self):
        """友好展示用户信息，避免空值异常"""
        # 优先级：用户名 → 手机号 → 用户ID
        display_name = self.username or self.phone or f"用户{self.pk}"
        return f"{display_name}"

    def clean(self):
        """数据清洗：保存前自动格式化字段"""
        super().clean()
        # 手机号格式化：去除空格/横线
        if self.phone:
            self.phone = self.phone.strip().replace("-", "").replace(" ", "")
        # 用户名去重空格
        if self.username:
            self.username = self.username.strip()

    # 修复核心权限方法：还原PermissionsMixin的默认逻辑
    def has_perm(self, perm, obj=None):
        """
        超级用户拥有所有权限，普通用户按权限表判断
        这是Django权限系统的核心方法，不能固定返回False
        """
        # 超级用户默认拥有所有权限
        if self.is_superuser:
            return True
        # 普通用户调用父类方法（PermissionsMixin）判断具体权限
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        """
        超级用户拥有所有app的权限，普通用户按权限表判断
        """
        # 超级用户默认拥有所有app的权限
        if self.is_superuser:
            return True
        # 普通用户调用父类方法判断
        return super().has_module_perms(app_label)

    # 保留适配框架的基础方法
    def get_full_name(self):
        """返回用户全名（适配框架，返回用户名/手机号）"""
        return self.username or self.phone

    def get_short_name(self):
        """返回用户简称（适配框架，手机号脱敏）"""
        return self.username or (self.phone[:3] + "****" + self.phone[-4:] if self.phone else "未知用户")