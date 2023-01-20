from rest_framework import serializers

class TagSerializer(serializers.Serializer):
    certificate_keys = serializers.JSONField()
   