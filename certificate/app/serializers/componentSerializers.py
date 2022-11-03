from rest_framework import serializers
from app.models import Component

from drf_extra_fields.fields import Base64ImageField


class ComponentSerializers(serializers.ModelSerializer):

    # image = Base64ImageField(
    #     required=False, max_length=None, use_url=True, allow_empty_file=True, allow_null=True,
    #     # represent_in_base64=True
    # )

    class Meta:
        model = Component
        fields = '__all__'
