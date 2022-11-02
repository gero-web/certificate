from rest_framework import serializers
from app.models import Certificate


class CertificateSerializers(serializers.ModelSerializer):

    class Meta:
        model = Certificate
        fields = '__all__'
