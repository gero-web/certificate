from rest_framework import serializers
from app.models import Certificate
from app.serializers.componentSerializers import ComponentSerializers

class CertificateSerializers(serializers.ModelSerializer):

    components = ComponentSerializers(many=True)
    class Meta:
        model = Certificate
        fields = ['certificate_key', 'email', 'exel', 'components']
