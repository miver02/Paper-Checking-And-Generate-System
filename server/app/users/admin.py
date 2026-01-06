from django.contrib import admin
from .models import User


@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "phone", "email", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["username", "phone", "email"]
    readonly_fields = ["created_at", "updated_at"]



