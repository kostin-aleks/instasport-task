"""

"""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from instasport.utils import slugify_name


class Country(models.Model):
    name = models.CharField(_("название"), max_length=200, db_index=True)
    iso = models.CharField(
        _("iso"), max_length=2, null=True, blank=True, db_index=True)

    class Meta:
        db_table = 'countries'
        verbose_name = _("Страна")
        verbose_name_plural = _("Страны")

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, verbose_name=_("страна"), null=True)
    name = models.CharField(_("название"), max_length=150, db_index=True)
    slug = models.SlugField(
        _("slug"), max_length=150, null=True, blank=True, unique=True)

    class Meta:
        db_table = 'cities'
        verbose_name = _("Город")
        verbose_name_plural = _("Города")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_name(City, self.name)
        return super().save(*args, **kwargs)


class SportClub(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, verbose_name=_("спортклуб"), null=True)
    name = models.CharField(_("название"), max_length=150, db_index=True)
    description = models.TextField(_('описание'), null=True, blank=True)
    slug = models.SlugField(
        _("slug"), max_length=150, null=True, blank=True, unique=True)

    class Meta:
        db_table = 'sportclubs'
        verbose_name = _("Спортклуб")
        verbose_name_plural = _("Спортклубы")

    def __str__(self):
        return self.name


class SportHall(models.Model):
    club = models.ForeignKey(
        SportClub, on_delete=models.SET_NULL, verbose_name=_("спортзал"), null=True)
    name = models.CharField(_("название"), max_length=150, db_index=True)
    description = models.TextField(_('описание'), null=True, blank=True)
    is_active = models.BooleanField(_('активный'), default=True)

    class Meta:
        db_table = 'sporthalls'
        verbose_name = _("Спортзал")
        verbose_name_plural = _("Спортзалы")

    def __str__(self):
        return self.name
