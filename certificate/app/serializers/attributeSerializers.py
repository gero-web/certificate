from rest_framework import serializers
from app.models import Attribute


class AttributeSerializers(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.color = validated_data.get('color', instance.color)
        instance.font = validated_data.get('font', instance.font)
        instance.font_size = validated_data.get('font_size', instance.font_size)
        instance.font_weight = validated_data.get('font_weight', instance.font_weight)
        instance.save()
        return instance

    class Meta:
        model = Attribute
        fields = '__all__'
