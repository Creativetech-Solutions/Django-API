from rest_framework import serializers
from django.contrib.auth.models import User

class Loginserializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=100)
    password = serializers.CharField(required=True, allow_blank=False, max_length=100)

    def login(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        return validated_data

