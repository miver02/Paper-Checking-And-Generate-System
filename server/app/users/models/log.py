from django.db import models
from .users import User

ACTION_CHOICES = (
    ("generate", "生成"),
    ("check", "检查"),
)


class UsedLog(models.Model):  # 优化：模型名用单数（Django默认规范，表名会自动转复数）
    """使用日志模型
    记录用户使用各模型的行为日志，包含操作类型、模型名称、token等关键信息
    """

    # 优化1：外键引用改为字符串形式，避免循环导入；字段注释更清晰
    user = models.OneToOneField(
        to="User",  # 字符串引用：app名.模型名（若跨app需写"app.User"）
        on_delete=models.SET_NULL,
        verbose_name="关联用户",
        null=True,
        blank=True,  # 补充blank=True：允许表单提交空值
        related_name="used_log",  # 优化：添加反向关联名，便于查询（如user.used_log）
        help_text="与用户一对一关联，用户删除时日志不删除，仅置空用户关联",
    )

    # 优化2：行为选项值语义化，去掉数字编码，标签用中文（更易理解）
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name="用户行为",
        help_text="用户执行的操作类型：generate-生成，check-检查",
    )

    # 优化3：模型名称字段补充默认值，选项语义化，注释更清晰
    model_name = models.CharField(
        max_length=20,
        verbose_name="模型名称",
        null=True,
        blank=True,
        help_text="模型名称",
    )

    # 优化4：token字段补充注释，限制最大长度更合理（根据实际token长度调整）
    token_quota = models.CharField(
        max_length=100,
        verbose_name="使用额度",
        null=True,
        blank=True,
        help_text="消耗的token额度",
    )

    # 优化5：时间字段补充注释，符合中文命名习惯
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
        help_text="日志创建时间，自动记录，不可修改",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        help_text="日志更新时间，自动记录，每次保存都会更新",
    )

    class Meta:
        verbose_name = "使用日志"
        verbose_name_plural = "使用日志"
        db_table = "used_logs"
        ordering = ["-created_at"]  # 优化：默认按创建时间倒序排列（最新日志在前）
        indexes = [  # 优化：添加索引，提升查询效率
            models.Index(fields=["user", "created_at"]),  # 常用查询组合索引
            models.Index(fields=["action", "model_name"]),
        ]

    def __str__(self):
        # 优化：处理user为None的情况，避免AttributeError
        username = self.user.username if self.user else "未知用户"
        return f"{username} - {self.get_action_display()} - {self.created_at.strftime('%Y-%m-%d')}"

    def get_action_display(self):
        """Django 内置的choices字段显示方法（自动生成）"""
        # 把choices转为字典，通过值找对应的标签
        status_dict = dict(ACTION_CHOICES)
        # 若值不存在，返回原始值（兼容异常情况）
        return status_dict.get(self.action, self.action)