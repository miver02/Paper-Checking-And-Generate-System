from django.contrib import admin
from .models import PlagiarismCheck, GeneratedPaper, User, UsedLog


@admin.register(GeneratedPaper)
class GeneratedPaperAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["title", "user__username", "requirements"]
    readonly_fields = ["created_at", "updated_at", "completed_at"]

    fieldsets = (
        (
            "基本信息",
            {"fields": ("user", "title", "requirements", "template", "status")},
        ),
        (
            "论文内容",
            {
                "fields": (
                    "abstract",
                    "key_words",
                    "abstract_en",
                    "key_words_en",
                    "content",
                    "summary",
                    "thank_words",
                    "literature",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "时间信息",
            {
                "fields": ("created_at", "updated_at", "completed_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(PlagiarismCheck)
class PlagiarismCheckAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "status", "similarity_percentage", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["title", "user__username"]
    readonly_fields = ["created_at", "updated_at", "completed_at"]

    fieldsets = (
        ("基本信息", {"fields": ("user", "title", "content", "status")}),
        (
            "检测结果",
            {
                "fields": ("similarity_percentage", "report_url", "report_data"),
                "classes": ("collapse",),
            },
        ),
        (
            "时间信息",
            {
                "fields": ("created_at", "updated_at", "completed_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "phone", "email", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["username", "phone", "email"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(UsedLog)
class UsedLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "model_name", "created_at"]
    list_filter = ["action", "model_name", "created_at"]
    search_fields = ["user__username", "model_name"]
    readonly_fields = ["created_at", "updated_at"]
