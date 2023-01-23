import collections
from rest_framework import serializers
import requests


class PdfEmailKeysSerializers(serializers.Serializer):
    keys = serializers.ListField()
  
class PdfGetCertificate(serializers.Serializer):
    key = serializers.JSONField()


class PdfGeneratorImageSerializers(serializers.Serializer):
    key = serializers.JSONField()
    email = serializers.JSONField()
    image = serializers.JSONField()
  
   
