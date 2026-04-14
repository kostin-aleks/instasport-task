"""
Application users. Serializers
"""

from rest_framework import serializers

from .models import Person


class CoachSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ["id", "full_name", "role"]
