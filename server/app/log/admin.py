from django.contrib import admin
from .models import UsedLog

@admin.register(UsedLog)
class UsedLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "model_name", "created_at"]
    list_filter = ["action", "model_name", "created_at"]
    search_fields = ["user__username", "model_name"]
    readonly_fields = ["created_at", "updated_at"]
