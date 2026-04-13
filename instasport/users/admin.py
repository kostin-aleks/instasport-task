"""

"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Person


@admin.register(Person)
class AdminPerson(admin.ModelAdmin):
    verbose_name = _('Пользователь')
    verbose_name_plural = _('Пользователи')
    list_display = ["id", "role", 'last_name', 'first_name', "middle_name", "is_active"]
    search_fields = ('first_name', 'last_name')
    ordering = ('-id', )





