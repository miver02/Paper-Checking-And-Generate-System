from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

# 抽离常量：提升可维护性，便于全局复用
PLAGIARISM_STATUS_CHOICES = (
    ("processing", "检测中"),
    ("completed", "已完成"),
    ("failed", "检测失败"),
)
# 相似度取值范围常量（0-100%）
SIMILARITY_MIN = 0
SIMILARITY_MAX = 100


class PlagiarismCheck(models.Model):
    """查重检测模型
    记录用户的文本查重检测请求、过程状态及检测结果，包含相似度、报告链接/数据等核心信息。
    """

    # 优化1：外键字符串引用（避免循环导入）+ 完善字段注释/约束
    user = models.ForeignKey(
        to="User",  # 推荐：字符串引用，彻底规避循环导入（跨app需写"app_name.User"）
        on_delete=models.SET_NULL,
        verbose_name="关联用户",
        related_name="plagiarism_checks",
        null=True,
        blank=True,  # 补充blank=True：允许表单层提交空值
        help_text="发起查重检测的用户，用户删除时仅置空关联，不删除检测记录",
    )

    # 优化2：标题字段补充约束+注释，限制合理长度（500字符偏长，可根据实际调整）
    title = models.CharField(
        max_length=500,
        verbose_name="检测标题",
        blank=True,  # 允许空标题（部分场景可能无标题）
        help_text="查重检测的文本标题，最长500个字符",
    )

    # 优化3：内容字段补充注释，明确用途
    content = models.TextField(
        verbose_name="检测内容", help_text="需要进行查重检测的文本内容，支持长文本"
    )

    # 优化4：相似度字段添加取值验证（0-100%），补充默认值和注释
    similarity_percentage = models.FloatField(
        verbose_name="相似度百分比",
        null=True,
        blank=True,
        default=None,
        validators=[
            MinValueValidator(SIMILARITY_MIN),
            MaxValueValidator(SIMILARITY_MAX),
        ],
        help_text=f"文本相似度百分比，取值范围[{SIMILARITY_MIN}, {SIMILARITY_MAX}]",
    )

    # 优化5：报告链接补充默认值+注释，限制URL长度
    report_url = models.URLField(
        verbose_name="详细报告链接",
        blank=True,
        default="",
        max_length=500,  # 限制URL长度，避免存储超长链接
        help_text="查重检测详细报告的访问链接，为空表示无报告链接",
    )

    # 优化6：JSON字段优化默认值（避免lambda潜在问题）+ 注释
    report_data = models.JSONField(
        verbose_name="检测报告数据",
        default=dict,  # 推荐：用dict代替lambda，避免序列化/迁移问题
        blank=True,
        help_text="查重检测的结构化报告数据（JSON格式），默认空字典",
    )

    # 优化7：状态字段补充注释，选项用常量
    status = models.CharField(
        max_length=20,
        choices=PLAGIARISM_STATUS_CHOICES,
        default="processing",
        verbose_name="检测状态",
        help_text="检测流程状态：processing-检测中，completed-已完成，failed-检测失败",
    )

    # 优化8：时间字段补充注释+约束，明确用途
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
        help_text="检测请求创建时间，自动记录，不可手动修改",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        help_text="检测记录更新时间，每次保存自动更新",
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="完成时间",
        help_text="检测完成时间，仅状态为「已完成」时自动填充",
    )

    class Meta:
        verbose_name = "查重检测记录"  
        verbose_name_plural = "查重检测记录"
        ordering = ["-created_at"]  # 保留：按创建时间倒序
        app_label = "users"
        db_table = "plagiarism_checks"  
        # 优化9：添加核心索引，提升查询效率
        indexes = [
            models.Index(fields=["user", "status"]),  # 常用查询：按用户+状态筛选
            models.Index(
                fields=["status", "created_at"]
            ),  # 常用查询：按状态+创建时间筛选
            models.Index(fields=["completed_at"]),  # 按完成时间筛选
        ]

    def __str__(self):
        """优化：更友好的字符串展示，处理空值避免异常"""
        # 处理相似度为空的情况，补充状态信息
        similarity = (
            f"{self.similarity_percentage:.1f}%"
            if self.similarity_percentage is not None
            else "未检测"
        )
        # 处理标题过长的情况，避免展示混乱
        short_title = self.title[:20] + "..." if len(self.title) > 20 else self.title
        return f"[{self.get_status_display()}] {short_title} - {similarity}"

    def save(self, *args, **kwargs):
        """优化：增强save逻辑的鲁棒性，补充边界条件处理"""
        # 仅当状态从非completed变为completed，且未设置完成时间时填充
        is_completed = self.status == "completed"
        need_set_completed_at = is_completed and not self.completed_at

        # 补充：若状态从completed改为其他，清空完成时间（符合业务逻辑）
        if not is_completed and self.completed_at:
            self.completed_at = None

        if need_set_completed_at:
            self.completed_at = timezone.now()

        # 调用父类save方法（核心逻辑保留）
        super().save(*args, **kwargs)

    # 优化10：新增便捷方法，提升业务代码复用性
    def is_completed(self):
        """快速判断检测是否完成"""
        return self.status == "completed"

    def is_failed(self):
        """快速判断检测是否失败"""
        return self.status == "failed"

    def get_similarity_display(self):
        """友好展示相似度（处理空值）"""
        if self.similarity_percentage is None:
            return "未检测"
        return f"{self.similarity_percentage:.1f}%"
    def get_status_display(self):
        """Django 内置的choices字段显示方法（自动生成）"""
        # 把choices转为字典，通过值找对应的标签
        status_dict = dict(PLAGIARISM_STATUS_CHOICES)
        # 若值不存在，返回原始值（兼容异常情况）
        return status_dict.get(self.status, self.status)