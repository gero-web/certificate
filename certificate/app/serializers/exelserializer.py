from rest_framework import serializers


class ExcelSerializers(serializers.Serializer):
    excel = serializers.FileField()
    layout_key = serializers.SlugField()
