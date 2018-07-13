from rest_framework import serializers

class Priceserializer(serializers.Serializer):
    data = serializers.CharField(required=True, allow_blank=False)

    def validate(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        return validated_data
