"""
Application locations. Admin models
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Country, City, SportClub, SportHall


@admin.register(Country)
class AdminCountry(admin.ModelAdmin):
    verbose_name = _("Страна")
    verbose_name_plural = _("Страны")
    list_display = ["id", "iso", "name"]
    search_fields = ("name", "iso")
    ordering = ("name",)


@admin.register(City)
class AdminCity(admin.ModelAdmin):
    verbose_name = _("Город")
    verbose_name_plural = _("Города")
    list_display = ["id", "name", "country"]
    search_fields = ("name",)
    ordering = ("name",)
    list_filter = ["country"]


@admin.register(SportClub)
class AdminSportClub(admin.ModelAdmin):
    verbose_name = _("Спортклуб")
    verbose_name_plural = _("Спортклубы")
    list_display = ["id", "name", "city"]
    search_fields = ("name", "description")
    ordering = ("name",)
    list_filter = ["city"]


@admin.register(SportHall)
class AdminSportHall(admin.ModelAdmin):
    verbose_name = _("Спортзал")
    verbose_name_plural = _("Спортзалы")
    list_display = ["id", "name", "club"]
    search_fields = ("name", "description")
    ordering = (
        "club",
        "name",
    )
    list_filter = ["club"]
