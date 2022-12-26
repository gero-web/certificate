from rest_framework import serializers


# class _TagSerializer(serializers.Serializer):
#     certificate_key = serializers.SlugField()

# class TagSerializer(serializers.Serializer):
#     certificate_keys = _TagSerializer(many=True)
class TagSerializer(serializers.Serializer):
    certificate_keys = serializers.JSONField()
