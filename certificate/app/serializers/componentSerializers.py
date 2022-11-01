from rest_framework import serializers
from app.models import Component, Body, SizeAndСoordinates, Attribute
from .sizeAndСoordinatesSerializers import SizeAndСoordinatesSerializers
from .attributeSerializers import AttributeSerializers
from .typeComponentSerializers import TypeComponentSerializers
from app.serializers.bodySerializers import BodySerializers


class ComponentSerializers(serializers.ModelSerializer):
    # type = TypeComponentSerializers(many=False)

    # body = BodySerializers(many=False)
    # size_and_coordinates = SizeAndСoordinatesSerializers(many=False)
    # attribute = AttributeSerializers(many=False)

    def create(self, validated_data):
        type = validated_data['type']

        # body = Body.objects.create(**validated_data['body'])
        # size_and_coordinates = SizeAndСoordinates.objects.create(**validated_data['size_and_coordinates'])
        # attribute = Attribute.objects.create(**validated_data['attribute'])

        body = validated_data['body']
        size_and_coordinates = validated_data['size_and_coordinates']
        attribute = validated_data['attribute']

        component = Component.objects.create(type=type, body=body, size_and_coordinates=size_and_coordinates, attribute=attribute)
        return component

    def update(self, instance, validated_data):

        # body = Body.objects.get(pk=instance.pk)
        # body.name = validated_data['body']['name']
        # body.image = validated_data['body']['image']
        # body.text = validated_data['body']['text']
        # body.save()
        #
        # SizeAndСoordinates.objects.filter(pk=instance.size_and_coordinates.pk).update(**validated_data['size_and_coordinates'])
        # Attribute.objects.filter(pk=instance.attribute.pk).update(**validated_data['attribute'])

        instance.body = validated_data['body']
        instance.size_and_coordinates = validated_data['size_and_coordinates']
        instance.attribute = validated_data['attribute']

        instance.type = validated_data['type']
        instance.save()

        return Component.objects.get(pk=instance.pk)

    class Meta:
        model = Component
        fields = (
            'type',
            'body',
            'size_and_coordinates',
            'attribute',
        )
        