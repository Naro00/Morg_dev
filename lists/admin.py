from django.contrib import admin
from . import models

@admin.register(models.List)
class ListAdmin(admin.ModelAdmin):
    """List admin definition"""
    
    list_display = ("name", "user", "count_academies")

    search_fields = ("name",)

    filter_horizontal = ("Academy",)
