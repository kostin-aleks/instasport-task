"""

"""
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Person(User):
    middle_name = models.CharField(max_length=32, null=True, blank=True)
    # role =
    created_at = models.DateTimeField(_('создание'), auto_now_add=True)
    updated_at = models.DateTimeField(_('изменение'), auto_now_add=True)

    class Meta:
        db_table = 'persons'
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")

    def __str__(self):
        return u'user %s: ' % (self.username)




