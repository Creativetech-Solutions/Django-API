from rest_framework import serializers

class Invoiceserializer(serializers.Serializer):
    staff_id = serializers.CharField(required=True, allow_blank=False, max_length=100)
    limit = serializers.CharField(required=False, allow_blank=True, max_length=100)
    search_str = serializers.CharField(required=False, allow_blank=True, max_length=100)
    client_id = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def validated(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        return validated_data

