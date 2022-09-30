from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Customer user admin definition"""

    fieldsets = UserAdmin.fieldsets + (
        ("Customer profile", {
            "fields": (
                "avatar", 
                "gender", 
                "bio", 
                "birthdate", 
                "language", 
                "Currency",
                "super_academy",
                "login_method"
            )
        }),
    )

    list_filter = UserAdmin.list_filter + ("super_academy",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "Currency",
        "super_academy",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method"
    )