"""
Application training. Serializers
"""

from rest_framework import serializers

from .models import SportsTraining, Sport
from instasport.locations.serializers import SportHallSerializer
from instasport.users.serializers import CoachSerializer


class TrainingListItemSerializer(serializers.ModelSerializer):
    weekday = serializers.SerializerMethodField()
    sportclub = serializers.SerializerMethodField()
    sport = serializers.SerializerMethodField()

    class Meta:
        model = SportsTraining
        fields = ["id", "weekday", "sportclub", "start_time", "end_time", "sport"]

    def get_weekday(self, obj):
        return {"name": SportsTraining.WeekDays(obj.weekday).label, "num": obj.weekday}

    def get_sportclub(self, obj):
        return obj.sporthall.club.name

    def get_sport(self, obj):
        return obj.sport.name


class FilterListSerializer(serializers.Serializer):
    weekday = serializers.CharField(required=False)
    sport = serializers.CharField(required=False)
    from_time = serializers.TimeField(required=False)
    to_time = serializers.TimeField(required=False)

    def validate_weekday(self, value):
        try:
            _ = [int(x) for x in value.split(",")]
        except ValueError:
            raise serializers.ValidationError(
                """Field "weekday" must be string that contains list of numbers separated by comma.
                   1-Sunday, 2-Monday, ...7-Saturday"""
            )
        return True

    def validate_sport(self, value):
        try:
            _ = [int(x) for x in value.split(",")]
        except ValueError:
            raise serializers.ValidationError(
                """Field "sport" must be string that contains list of id separated by comma.
                   Look at docs to get id of sport"""
            )
        return True


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ["id", "name", "slug"]


class TrainingForClientSerializer(serializers.ModelSerializer):
    weekday = serializers.SerializerMethodField()
    sporthall = SportHallSerializer()
    sport = SportSerializer()
    coach = CoachSerializer()

    class Meta:
        model = SportsTraining
        fields = [
            "id",
            "description",
            "sporthall",
            "weekday",
            "start_time",
            "end_time",
            "coach",
            "sport",
        ]

    def get_weekday(self, obj):
        return {"name": SportsTraining.WeekDays(obj.weekday).label, "num": obj.weekday}


class WeekDaySerializer(serializers.Serializer):
    num = serializers.IntegerField()
    name = serializers.CharField()
