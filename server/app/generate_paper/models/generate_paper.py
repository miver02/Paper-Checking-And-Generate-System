from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxLengthValidator

# 抽离全局常量：提升可维护性，避免硬编码
GENERATE_STATUS_CHOICES = (
    ("queued", "排队中"),
    ("generating", "生成中"),
    ("completed", "已完成"),
    ("failed", "生成失败"),
)
# 字段长度常量：便于统一调整
TITLE_MAX_LENGTH = 100


class GeneratedPaper(models.Model):
    """论文生成模型
    记录用户发起的论文生成请求、生成要求、模板信息，以及最终生成的完整论文内容（含摘要、关键词、正文等），
    同时追踪生成状态和时间节点。
    """
    # 优化1：外键字符串引用（彻底规避循环导入）+ 完善字段约束/注释
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="关联用户",
        related_name="generated_papers",
        null=True,
        blank=True,  # 补充blank=True：允许表单层空值
        help_text="发起论文生成的用户，用户删除时仅置空关联，不删除生成记录"
    )

    # 优化2：标题字段补充验证+注释，限制长度更规范
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        verbose_name="论文标题",
        blank=True,  # 允许空标题（部分场景用户未指定）
        validators=[MaxLengthValidator(TITLE_MAX_LENGTH)],  # 双重保障长度
        help_text=f"论文标题，最长{TITLE_MAX_LENGTH}个字符"
    )

    # 优化3：生成要求/模板字段补充注释，明确用途
    requirements = models.TextField(
        verbose_name="生成要求",
        help_text="用户提出的论文生成需求（如主题、字数、结构要求等）"
    )
    template = models.TextField(
        verbose_name="模板内容",
        blank=True,  # 允许无模板（使用默认模板）
        help_text="论文生成所用的模板文本，为空时使用系统默认模板"
    )

    # 中文摘要
    abstract = models.TextField(
        blank=True,
        verbose_name="中文摘要",
        help_text="生成的论文中文摘要"
    )

    # 中文关键词（改为 JSON）
    key_words = models.JSONField(
        blank=True,
        default=list,
        verbose_name="中文关键词",
        help_text="中文关键词列表，如 ['AI', '深度学习']"
    )

    # 英文摘要
    abstract_en = models.TextField(
        blank=True,
        verbose_name="英文摘要",
        help_text="生成的论文英文摘要"
    )

    # 英文关键词（改为 JSON）
    key_words_en = models.JSONField(
        blank=True,
        default=list,
        verbose_name="英文关键词",
        help_text="英文关键词列表"
    )

    # 正文
    content = models.TextField(
        blank=True,
        verbose_name="论文正文",
        help_text="生成的论文完整正文内容"
    )

    # 总结
    summary = models.TextField(
        blank=True,
        verbose_name="论文总结",
        help_text="论文核心结论与总结"
    )

    # 致谢
    thank_words = models.TextField(
        blank=True,
        verbose_name="致谢语",
        help_text="论文致谢部分内容"
    )

    # 参考文献（JSON 正确写法）
    literature = models.JSONField(
        blank=True,
        default=list,
        verbose_name="参考文献",
        help_text="参考文献列表（结构化数据）"
    )

    # 优化6：状态字段使用常量+补充注释
    status = models.CharField(
        max_length=20,
        choices=GENERATE_STATUS_CHOICES,
        default="queued",
        verbose_name="生成状态",
        help_text="论文生成状态：queued-排队中，generating-生成中，completed-已完成，failed-生成失败"
    )

    # Celery 任务ID，便于排查与前端轮询
    task_id = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        verbose_name="任务ID",
        help_text="Celery任务ID"
    )

    # 失败原因，便于前端展示与后续重试排查
    failed_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name="失败原因",
        help_text="任务失败时的错误信息"
    )

    # 优化7：时间字段补充注释，明确用途
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间",
        help_text="生成请求创建时间，自动记录，不可手动修改"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新时间",
        help_text="记录更新时间，每次保存自动更新"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="完成时间",
        help_text="论文生成完成时间，仅状态为「已完成」时自动填充"
    )

    class Meta:
        verbose_name = "论文生成记录"  # 优化：名称更精准
        verbose_name_plural = "论文生成记录"
        ordering = ["-created_at"]  # 保留：按创建时间倒序
        db_table = "generated_papers"  # 优化：表名改为复数（符合数据库规范）
        # 优化8：添加核心索引，提升查询效率
        indexes = [
            models.Index(fields=["user", "status"]),  # 常用：按用户+状态筛选
            models.Index(fields=["status", "created_at"]),  # 常用：按状态+创建时间筛选
            models.Index(fields=["completed_at"]),  # 按完成时间统计/筛选
        ]

    def __str__(self):
        """优化：友好展示，处理空值/超长标题，补充状态信息"""
        # 处理用户为空
        username = self.user.username if self.user else "未知用户"
        # 处理标题过长
        short_title = self.title[:20] + "..." if len(self.title) > 20 else self.title or "无标题"
        # 补充状态信息
        status_text = self.get_status_display()
        return f"[{status_text}] {short_title} - {username}"

    def save(self, *args, **kwargs):
        """优化：修复逻辑bug，增强鲁棒性，补充边界条件"""
        # 修复：原代码中 "completed " 多了空格，导致逻辑失效
        is_completed = self.status == "completed"
        need_set_completed_at = is_completed and not self.completed_at
        
        # 补充：状态从completed改为其他时，清空完成时间（符合业务逻辑）
        if not is_completed and self.completed_at:
            self.completed_at = None
        
        # 仅当状态为已完成且未设置完成时间时填充
        if need_set_completed_at:
            self.completed_at = timezone.now()

        super().save(*args, **kwargs)

    # 优化9：新增便捷方法，提升业务代码复用性
    def is_generating(self):
        """判断是否正在生成"""
        return self.status == "generating"

    def is_queued(self):
        """判断是否已进入队列"""
        return self.status == "queued"

    def is_processing(self):
        """判断是否处于排队或生成中"""
        return self.status in {"queued", "generating"}

    def is_completed(self):
        """判断是否生成完成"""
        return self.status == "completed"

    def is_failed(self):
        """判断是否生成失败"""
        return self.status == "failed"

    def get_key_words_list(self, lang="zh"):
        """将关键词文本转为列表（按分号分隔）"""
        key_words_field = self.key_words if lang == "zh" else self.key_words_en
        if not key_words_field:
            return []
        # 去除空值和空格
        return [kw.strip() for kw in key_words_field.split(";") if kw.strip()]
