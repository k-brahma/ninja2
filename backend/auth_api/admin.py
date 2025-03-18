from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """カスタムユーザー管理画面の設定"""

    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("id",)


admin.site.register(CustomUser, CustomUserAdmin)
