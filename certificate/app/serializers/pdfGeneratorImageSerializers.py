import collections
from rest_framework import serializers
import requests




class PdfGeneratorImageSerializers(serializers.Serializer):
    image = serializers.ListField()
  
   
