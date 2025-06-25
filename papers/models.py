from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PaperTopic(models.Model):
    """论文主题模型"""
    name = models.CharField(max_length=200, verbose_name='主题名称')
    description = models.TextField(blank=True, verbose_name='主题描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '论文主题'
        verbose_name_plural = '论文主题'
    
    def __str__(self):
        return self.name


class GeneratedPaper(models.Model):
    """生成的论文模型"""
    STATUS_CHOICES = [
        ('generating', '生成中'),
        ('completed', '已完成'),
        ('failed', '生成失败'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField(max_length=500, verbose_name='论文标题')
    topic = models.ForeignKey(PaperTopic, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='论文主题')
    requirements = models.TextField(verbose_name='生成要求')
    content = models.TextField(blank=True, verbose_name='论文内容')
    word_count = models.IntegerField(default=0, verbose_name='字数')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='generating', verbose_name='状态')
    
    # 生成参数
    model_used = models.CharField(max_length=100, default='gpt-3.5-turbo', verbose_name='使用的模型')
    temperature = models.FloatField(default=0.7, verbose_name='创造性参数')
    max_tokens = models.IntegerField(default=4000, verbose_name='最大令牌数')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        verbose_name = '生成的论文'
        verbose_name_plural = '生成的论文'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        if self.content:
            self.word_count = len(self.content.replace(' ', ''))
        super().save(*args, **kwargs)


class PlagiarismCheck(models.Model):
    """查重检测模型"""
    STATUS_CHOICES = [
        ('pending', '待检测'),
        ('processing', '检测中'),
        ('completed', '已完成'),
        ('failed', '检测失败'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    paper = models.ForeignKey(GeneratedPaper, on_delete=models.CASCADE, null=True, blank=True, verbose_name='关联论文')
    title = models.CharField(max_length=500, verbose_name='检测标题')
    content = models.TextField(verbose_name='检测内容')
    
    # 检测结果
    similarity_percentage = models.FloatField(null=True, blank=True, verbose_name='相似度百分比')
    report_url = models.URLField(blank=True, verbose_name='详细报告链接')
    report_data = models.JSONField(default=dict, blank=True, verbose_name='检测报告数据')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    api_used = models.CharField(max_length=100, blank=True, verbose_name='使用的API')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    
    class Meta:
        verbose_name = '查重检测'
        verbose_name_plural = '查重检测'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.similarity_percentage}%" if self.similarity_percentage else self.title
    
    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """用户配置模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    
    # 使用统计
    papers_generated = models.IntegerField(default=0, verbose_name='生成论文数')
    plagiarism_checks = models.IntegerField(default=0, verbose_name='查重次数')
    
    # 偏好设置
    preferred_model = models.CharField(max_length=100, default='gpt-3.5-turbo', verbose_name='偏好模型')
    default_temperature = models.FloatField(default=0.7, verbose_name='默认创造性参数')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户配置'
        verbose_name_plural = '用户配置'
    
    def __str__(self):
        return f"{self.user.username}的配置" 