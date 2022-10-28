from rest_framework import serializers
from django.conf import settings
from app.models import Component, Body, SizeAndСoordinates, Attribute, upload_to
from .sizeAndСoordinatesSerializers import SizeAndСoordinatesSerializers
from .attributeSerializers import AttributeSerializers
from app.serializers.bodySerializers import BodySerializers
from django.core.files.base import ContentFile, File
import os


class ComponentSerializers(serializers.ModelSerializer):
    body = BodySerializers(many=False)
    size_and_coordinates = SizeAndСoordinatesSerializers(many=False)
    attribute = AttributeSerializers(many=False)

    def create(self, validated_data):
        body = Body.objects.create(**validated_data['body'])
        size_and_coordinates = SizeAndСoordinates.objects.create(**validated_data['size_and_coordinates'])
        attribute = Attribute.objects.create(**validated_data['attribute'])
        component = Component.objects.create(body=body, size_and_coordinates=size_and_coordinates, attribute=attribute)
        return component

    def update(self, instance, validated_data):

        body = Body.objects.get(pk=1)
        body.name = validated_data['body']['name']
        body.image = validated_data['body']['image']
        body.text = validated_data['body']['text']
        body.save()

        SizeAndСoordinates.objects.filter(pk=instance.size_and_coordinates.pk).update(**validated_data['size_and_coordinates'])
        Attribute.objects.filter(pk=instance.attribute.pk).update(**validated_data['attribute'])

        return Component.objects.get(pk=instance.pk)

    class Meta:
        model = Component
        fields = (
            'body',
            'size_and_coordinates',
            'attribute',
        )
