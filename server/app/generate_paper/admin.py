from django.contrib import admin
from .models import GeneratedPaper


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
