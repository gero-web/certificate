from rest_framework import serializers


class ExcelSerializers(serializers.Serializer):
    layout_key = serializers.SlugField()
    email = serializers.EmailField(required=False)
