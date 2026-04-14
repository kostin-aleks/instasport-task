"""
Application users. ORM models
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(User):
    """
    Person
    """

    class Role(models.TextChoices):
        CUSTOMER = ("customer", _("Клиент"))
        COACH = ("coach", _("Тренер"))

    middle_name = models.CharField(max_length=32, null=True, blank=True)
    role = models.CharField(
        _("роль"),
        max_length=30,
        choices=Role.choices,
        default=Role.CUSTOMER,
        db_index=True,
    )
    created_at = models.DateTimeField(_("создание"), auto_now_add=True)
    updated_at = models.DateTimeField(_("изменение"), auto_now_add=True)

    class Meta:
        db_table = "persons"
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return f"user {self.username}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"
