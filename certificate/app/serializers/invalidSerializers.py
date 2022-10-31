from rest_framework import serializers


class InvalidSerializer(serializers.Serializer):
    msg = serializers.CharField(read_only=True)
