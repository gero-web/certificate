from rest_framework import serializers
from app.models import Body


class BodySerializers(serializers.ModelSerializer):

    class Meta:
        model = Body
        fields = '__all__'
