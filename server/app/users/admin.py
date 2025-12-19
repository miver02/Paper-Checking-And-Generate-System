from django.contrib import admin
from .models.generate_paper import PaperTopic, GeneratedPaper, PlagiarismCheck, UserProfile


@admin.register(PaperTopic)
class PaperTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']


@admin.register(GeneratedPaper)
class GeneratedPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'topic', 'status', 'word_count', 'created_at']
    list_filter = ['status', 'topic', 'model_used', 'created_at']
    search_fields = ['title', 'user__username', 'requirements']
    readonly_fields = ['word_count', 'created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'title', 'topic', 'requirements', 'status')
        }),
        ('生成参数', {
            'fields': ('model_used', 'temperature', 'max_tokens'),
            'classes': ('collapse',)
        }),
        ('内容', {
            'fields': ('content', 'word_count'),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PlagiarismCheck)
class PlagiarismCheckAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'similarity_percentage', 'created_at']
    list_filter = ['status', 'api_used', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user', 'paper', 'title', 'status')
        }),
        ('检测结果', {
            'fields': ('similarity_percentage', 'report_url', 'api_used'),
            'classes': ('collapse',)
        }),
        ('内容', {
            'fields': ('content',),
            'classes': ('collapse',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'papers_generated', 'plagiarism_checks', 'created_at']
    list_filter = ['preferred_model', 'created_at']
    search_fields = ['user__username', 'bio']
    readonly_fields = ['papers_generated', 'plagiarism_checks', 'created_at', 'updated_at'] 