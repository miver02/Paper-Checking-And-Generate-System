from django.conf import settings
from django.db import models


class ActionType(models.TextChoices):
    GENERATE = "generate", "生成"
    CHECK = "check", "检查"


class UsedLog(models.Model):
    """使用日志模型"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="关联用户",
        null=True,
        blank=True,
        related_name="used_logs",
    )

    action = models.CharField(
        max_length=20,
        choices=ActionType.choices,
        verbose_name="用户行为",
    )

    action_id = models.IntegerField(
        verbose_name="操作ID",
        null=True,
        blank=True,
    )

    model_name = models.CharField(
        max_length=50,
        verbose_name="模型名称",
        null=True,
        blank=True,
    )

    token_quota = models.IntegerField(
        verbose_name="消耗token",
        null=True,
        blank=True,
    )

    ip_addr = models.GenericIPAddressField(
        verbose_name="IP地址",
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        verbose_name="用户代理",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
    )

    class Meta:
        db_table = "used_logs"
        verbose_name = "使用日志"
        verbose_name_plural = "使用日志"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["user", "action"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user_id or '匿名'} - {self.action} - {self.created_at:%Y-%m-%d}"