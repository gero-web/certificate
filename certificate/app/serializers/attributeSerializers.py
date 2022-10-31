from rest_framework import serializers
from app.models import Attribute


class AttributeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = '__all__'
