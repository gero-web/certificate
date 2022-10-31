from rest_framework import serializers
from app.models import TypeComponent


class TypeComponentSerializers(serializers.ModelSerializer):

    class Meta:
        model = TypeComponent
        fields = '__all__'
