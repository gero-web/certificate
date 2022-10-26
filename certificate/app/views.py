from venv import create
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST,HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .serializers import  LayoutSerializers, HtmlSerializers,AttributeSerializers,ComponentSeralizers
from .models import Layout
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class ComponentViewsSet(ModelViewSet):
  
    
    queryset = Layout.objects.all()
    serializer_class = LayoutSerializers
    permission_classes = [
        permissions.AllowAny,
    ]
    
    parser_classes = (
                        FormParser, 
                        MultiPartParser, 
                    )
    
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        request=LayoutSerializers,
        responses={201: LayoutSerializers},
    )
  
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
  
  
    
  
        