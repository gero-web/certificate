from rest_framework import serializers
from ..models import Component


class ComponentSerializers(serializers.ModelSerializer):

    # type = TypeComponentSerializers()

    def update(self, instance, validated_data):
        # instance.TypeComponent = validated_data.get('type', instance.type)
        instance.x = validated_data.get('x', instance.x)
        instance.y = validated_data.get('y', instance.y)
        instance.z = validated_data.get('z', instance.z)
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.save()
        return instance

    class Meta:
        model = Component
        fields = '__all__'
