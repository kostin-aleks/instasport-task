"""
Application training. Views
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from .filters import TrainingFilters
from .models import SportsTraining, Sport
from .serializers import (
    TrainingListItemSerializer,
    FilterListSerializer,
    TrainingForClientSerializer,
    SportSerializer,
    WeekDaySerializer,
)


class TrainingView(APIView):
    http_method_names = [
        "get",
    ]

    def get_queryset(self):
        queryset = (
            SportsTraining.objects.filter(is_active=True, sporthall__is_active=True)
            .select_related("coach", "sport", "sporthall__club")
            .order_by("weekday", "start_time")
        )
        return queryset

    def get(self, request, format=None):
        """
        Get list of training
        filtered by weekday, sport, from_time, to_time
        """
        filters_from_request = request.query_params.dict()
        serializer = FilterListSerializer(data=filters_from_request)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()
        filtered_qs = TrainingFilters(filters_from_request, queryset=queryset).qs[:1000]

        serializer = TrainingListItemSerializer(filtered_qs, many=True)
        return Response(serializer.data)


class TrainingByIdView(RetrieveAPIView):
    """
    get: Retrieve training by id
    """

    serializer_class = TrainingForClientSerializer

    def get_queryset(self):
        return (
            SportsTraining.objects.filter(is_active=True, sporthall__is_active=True)
            .select_related(
                "coach",
                "sport",
                "sporthall",
                "sporthall__club",
                "sporthall__club__city",
                "sporthall__club__city__country",
            )
            .order_by("weekday", "start_time")
        )


class SportsView(APIView):
    http_method_names = [
        "get",
    ]

    def get_queryset(self):
        queryset = Sport.objects.all().order_by("slug")
        return queryset

    def get(self, request, format=None):
        """
        Get list of sport
        """
        serializer = SportSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class WeekDayView(APIView):
    http_method_names = [
        "get",
    ]

    def get_queryset(self):
        return Sport.objects.none()

    def get(self, request, format=None):
        """
        Get list of week days
        """
        days = [
            {"num": item[0], "name": item[1]}
            for item in SportsTraining.WeekDays.choices
        ]
        serializer = WeekDaySerializer(days, many=True)

        return Response(serializer.data)
