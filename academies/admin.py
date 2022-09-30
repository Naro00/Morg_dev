from django.contrib import admin
from django.utils.html import mark_safe
from . import models

@admin.register(models.Event, models.Facility, models.Amenity)
class ItemAdmin(admin.ModelAdmin):
    """Item Admin definition"""

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.academies.count()

    pass


@admin.register(models.Academy)
class AcademyAdmin(admin.ModelAdmin):
    """Academy admin definition"""

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "city", "borough", "events", "adress", "price")},
        ),
        ("Times", {"fields": ("booking", "instant_book")}),
        ("Spaces", {"fields": ("guests", )}),
        ("More about the Space", {
            "classes": ("collapse",),
            "fields": ("amenities", "facility")
        }),
        ("Last Details", {"fields": ("host",)}),
    )
    
    list_display = (
        "name",
        "city",
        "borough",
        "events",
        "price",
        "guests",
        "booking",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "events",
        "amenities",
        "facility",
        "city",
        "borough",
    )

    raw_id_fields = ("host",)

    search_fields = ("city", "^host_username")

    filter_horizontal = ("amenities", "facility")

    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()
    count_photos.short_description = "Photo Count"

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """Photo admin definition"""

    list_display = ("__str__", "get_thmbnail")

    def get_thmbnail(self, obj):
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')
    get_thmbnail.short_description = "Thumbnail"