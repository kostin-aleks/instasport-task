"""
Application training. Admin models
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Sport, SportsTraining


@admin.register(Sport)
class AdminSport(admin.ModelAdmin):
    verbose_name = _("Вид спорта")
    verbose_name_plural = _("Виды спорта")
    list_display = ["id", "name", "slug"]
    search_fields = ("name", "slug")
    ordering = ("-id",)


@admin.register(SportsTraining)
class AdminSportsTraining(admin.ModelAdmin):
    verbose_name = _("Тренировка")
    verbose_name_plural = _("Тренировки")
    list_display = [
        "id",
        "sportclub",
        "weekday",
        "start_time",
        "end_time",
        "sport",
        "is_active",
    ]
    ordering = ("weekday", "start_time")
    list_filter = [
        "sport",
        "weekday",
        "sporthall__club",
        "is_active",
    ]
