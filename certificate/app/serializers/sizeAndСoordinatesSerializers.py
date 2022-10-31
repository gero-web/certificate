from rest_framework import serializers
from app.models import SizeAndСoordinates


class SizeAndСoordinatesSerializers(serializers.ModelSerializer):

    class Meta:
        model = SizeAndСoordinates
        fields = '__all__'
