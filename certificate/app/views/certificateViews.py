from email import header
import json
import uuid
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser,JSONParser
from rest_framework.viewsets import ModelViewSet
from app.serializers.certificateSerializers import CertificateSerializers
from app.serializers.exelserializer import ExcelSerializers
from app.serializers.invalidSerializers import InvalidSerializer
from app.models import Certificate,Component
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile;
from django.http.response import JsonResponse
import pandas as pd
class CertificateViewsSet(ModelViewSet):

    queryset = Certificate.objects.all().order_by('pk')
    serializer_class = CertificateSerializers
    permission_classes = [
        permissions.AllowAny,
    ]
    lookup_field = 'certificate_key'

    parser_classes = (
        MultiPartParser,
        JSONParser,
       
    )
    
    renderer_classes = (
        TemplateHTMLRenderer,
        JSONRenderer,
    )
    
    @extend_schema(
        description='',
        responses={status.HTTP_200_OK: {'certificates': f'pk: {uuid.uuid4}'}, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().values_list('pk', 'certificate_key')  
        return JsonResponse(data={'certificates': dict(queryset)})
    

    @extend_schema(
        request=CertificateSerializers,
        responses={status.HTTP_200_OK: CertificateSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super(CertificateViewsSet, self).update(request, *args, **kwargs)

    @extend_schema(
        request=CertificateSerializers,
        responses={status.HTTP_200_OK: CertificateSerializers, status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        certificate_key = kwargs['certificate_key']
        print(certificate_key)
        components = Component.objects.filter(certificate__certificate_key=certificate_key)
        if not components:
            return JsonResponse(data={'msg': 'certificate not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'components': components}, template_name='crificate.html')

    @extend_schema(
        request=ExcelSerializers,
        responses={status.HTTP_201_CREATED: uuid.uuid4(), status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        excelSerializer = ExcelSerializers(data=request.data)
        if excelSerializer.is_valid():
            components = Component.objects.filter(layout__layout_key=excelSerializer.data['layout_key'])
            if components:     
                cer = Certificate.objects.create(certificate_key=uuid.uuid4())
                for component in components:
                    cer.components.add(component)
                return JsonResponse({'certificate_key': cer.certificate_key}, status=status.HTTP_201_CREATED)

        return JsonResponse(data={'msg': 'layout not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @extend_schema(
        request=CertificateSerializers,
        responses={status.HTTP_204_NO_CONTENT: CertificateSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):
        return super(CertificateViewsSet, self).destroy(request, *args, **kwargs)

    
   