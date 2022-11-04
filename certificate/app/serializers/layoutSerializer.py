from app.models import Layout
from rest_framework import serializers
from .componentSerializers import ComponentSerializers
from .certificateSerializers import CertificateSerializers


class LayoutSerializer(serializers.ModelSerializer):
    component = ComponentSerializers(many=True, required=True, read_only=False)
    layout_key = serializers.SlugField(read_only=True, required=False)

    class Meta:
        model = Layout
        fields = (
                    'layout_key',
                    'component',
                 )

