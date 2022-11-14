import collections
from app.models import Component
from rest_framework import serializers
import requests


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import re
        import base64
        import six
        import uuid
        from urllib.parse import urlparse

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')
                decoded_file = base64.b64decode(data)
                decoded_file = base64.b64decode(data)
                # Generate file name:
                file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
                # Get the file name extension:
                file_extension = self.get_file_extension(file_name, decoded_file)

                complete_file_name = "%s.%s" % (file_name, file_extension,)

                data = ContentFile(decoded_file, name=complete_file_name)
            else:
                # Try to decode the file. Return validation error if it fails.
                regex = re.compile(
                    r'^(?:http|ftp)s?://'  # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                    r'localhost|'  # localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                    r'(?::\d+)?'  # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                if re.match(regex, data) is not None:
                    response = requests.get(data)
                    if response.status_code == 200:
                        name = urlparse(data).path.split('/')[-1]
                        data = ContentFile(response.content, name=name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class ComponentSerializers(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['type'] = instance.type.name
        # or replace the name with your pricing name field

        return data

    class Meta:
        model = Component
        fields = '__all__'
