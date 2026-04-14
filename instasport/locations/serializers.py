"""
Application locations. Serializers
"""

from rest_framework import serializers

from .models import SportClub, SportHall, City, Country


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ["id", "name", "iso"]


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ["id", "name", "slug", "country"]


class SportClubSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = SportClub
        fields = ["id", "name", "slug", "city", "description"]


class SportHallSerializer(serializers.ModelSerializer):
    club = SportClubSerializer()

    class Meta:
        model = SportHall
        fields = ["id", "name", "club", "description"]
