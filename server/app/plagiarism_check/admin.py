from django.contrib import admin
from .models import PlagiarismCheck


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
