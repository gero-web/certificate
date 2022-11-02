from app.models import Layout
from rest_framework import serializers
from .componentSerializers import ComponentSerializers
from .certificateSerializers import CertificateSerializers


class LayoutSerializer(serializers.ModelSerializer):
    # component = ComponentSerializers(many=False)
    # certificate = CertificateSerializers(many=False)

    def create(self, validated_data):
        component = validated_data['component']
        certificate = validated_data['certificate']
        layout = Layout.objects.create(component=component, certificate=certificate)
        return layout

    def update(self, instance, validated_data):
        instance.component = validated_data['component']
        instance.certificate = validated_data['certificate']
        instance.save()
        return Layout.objects.get(pk=instance.pk)

    class Meta:
        model = Layout
        fields = '__all__'
