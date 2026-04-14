"""
Application training. Urls
"""

from django.urls import path

from .views import (
    TrainingView,
    TrainingByIdView,
    SportsView,
    WeekDayView,
)  # , week_days

urlpatterns = [
    path("", TrainingView.as_view(), name="get-list-trainings"),
    path("<int:id>", TrainingByIdView.as_view(), name="get-training-by-id"),
    path("sport", SportsView.as_view(), name="get-list-sport"),
    path("weekdays", WeekDayView.as_view(), name="get-week-days"),
]
