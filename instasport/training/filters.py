"""
Application training. Filters
"""

from django.db.models.query import QuerySet
from django_filters import rest_framework as filters

from .models import SportsTraining


class TrainingFilters(filters.FilterSet):
    weekday = filters.CharFilter(method="filter_weekday")
    from_time = filters.CharFilter(method="filter_from_time")
    to_time = filters.CharFilter(method="filter_to_time")
    sport = filters.CharFilter(method="filter_sport")

    class Meta:
        model = SportsTraining
        fields = [
            "weekday",
        ]

    @staticmethod
    def filter_weekday(queryset: QuerySet, _, value: str):
        values = value.split(",")
        values = [int(x) for x in values]
        if not values:
            return queryset
        return queryset.filter(weekday__in=values)

    @staticmethod
    def filter_sport(queryset: QuerySet, _, value: str):
        values = value.split(",")
        values = [int(x) for x in values]
        if not values:
            return queryset
        return queryset.filter(sport__in=values)

    @staticmethod
    def filter_from_time(queryset: QuerySet, _, value: str):
        if not value:
            return queryset
        return queryset.filter(start_time__gte=value)

    @staticmethod
    def filter_to_time(queryset: QuerySet, _, value: str):
        if not value:
            return queryset
        return queryset.filter(start_time__lte=value)
