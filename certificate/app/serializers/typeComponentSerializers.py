from rest_framework import serializers
from ..models import TypeComponent


class TypeComponentSerializers(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

    class Meta:
        model = TypeComponent
        fields = '__all__'
