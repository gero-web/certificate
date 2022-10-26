from rest_framework import serializers
from ..models import Html


class HtmlSerializers(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('name', instance.name)
        instance.image = validated_data.get('name', instance.name)
        instance.save()
        return instance

    class Meta:
        model = Html
        fields = '__all__'
