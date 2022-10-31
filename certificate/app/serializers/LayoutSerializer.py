from app.models import Layout
from rest_framework import serializers

class LayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layout
        fields = '__all__'
