"""

"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


from instasport.users.models import Person
from instasport.locations.models import SportHall
from instasport.utils import slugify_name


class Sport(models.Model):
    """

    """
    name = models.CharField(_('название'), max_length=255)
    slug = models.SlugField(
        _("slug"), max_length=150, null=True, blank=True, unique=True)
    description = models.TextField(
        _("описание"), null=True, blank=True)

    class Meta:
        db_table = 'sports'
        verbose_name = _("Вид спорта")
        verbose_name_plural = _("Виды спорта")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_name(Sport, self.name)
        return super().save(*args, **kwargs)


class SportsTraining(models.Model):
    """

    """
    class WeekDays(models.IntegerChoices):
        SUNDAY = (1, _("Воскресенье"))
        MONDAY = (2, _("Понедельник"))
        TUESDAY = (3, _("Вторник"))
        WEDNESDAY = (4, _("Среда"))
        THURSDAY = (5, _("Четверг"))
        FRIDAY = (6, _("Пятница"))
        SATURDAY = (7, _("Суббота"))

    description = models.TextField(
        _("описание"), null=True, blank=True)
    sporthall = models.ForeignKey(
        SportHall, on_delete=models.SET_NULL, verbose_name=_("спортзал"), null=True)
    weekday = models.PositiveIntegerField(choices=WeekDays.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    coach = models.ForeignKey(
        Person, on_delete=models.SET_NULL, verbose_name=_("тренер"), null=True)
    sport = models.ForeignKey(
        Sport, on_delete=models.SET_NULL, verbose_name=_("вид спорта"), null=True)
    is_active = models.BooleanField(_('активный'), default=True)
    created_at = models.DateTimeField(_('создание'), auto_now_add=True)
    updated_at = models.DateTimeField(_('изменение'), auto_now_add=True)

    class Meta:
        db_table = 'trainings'
        verbose_name = _("Тренировка")
        verbose_name_plural = _("Тренировки")

    def __str__(self) -> str:
        return f"{self.id}-{self.weekday}/{self.start_time}-{self.end_time}"

    @property
    def sportclub(self):
        """"""
        return self.sporthall.club.name

    @property
    def duration(self):
        """durations, minutes"""
        return (self.end_time - self.start_time).seconds // 60
