from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.viewsets import ModelViewSet
from app.serializers.certificateSerializers import CertificateSerializers
from app.serializers.exelserializer import ExcelSerializers
from app.serializers.invalidSerializers import InvalidSerializer
from app.models import Certificate, Component
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from app.helpers.html_certificate import html_template_certificate
import uuid


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
        description='Возвращает список сертификатов!',
        responses={status.HTTP_200_OK: {'certificates': f'pk: {uuid.uuid4}'},
                   status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        queryset = Certificate.objects.all().values_list('certificate_key').distinct('certificate_key')
        print(queryset)
        return JsonResponse(data={'certificates': list(queryset)})

    @extend_schema(
        request=CertificateSerializers,
        description='Не реализован и не должен проверятся на данный момент!',
        responses={status.HTTP_200_OK: CertificateSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super(CertificateViewsSet, self).update(request, *args, **kwargs)

    @extend_schema(
        description='Возвращает конкретный сертификат виде html страницы, если сертификат не найдет вернет JSON',
        responses={status.HTTP_200_OK:{},
                   status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        certificate_key = kwargs['certificate_key']
        template = html_template_certificate(certificate_key)
        if template is None:
            return JsonResponse(data={'msg': 'certificate not found'}, status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(template)

    @extend_schema(
        request=ExcelSerializers,
        description='Создает сертификат email необязательное',
        responses={status.HTTP_201_CREATED: uuid.uuid4(), status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        exelSerializer = ExcelSerializers(data=request.data)
        if exelSerializer.is_valid():
            components = Component.objects.filter(layout__layout_key=exelSerializer.data['layout_key'])
            email = exelSerializer.data['email']
            if components:
                if email:
                    cer = Certificate.objects.create(certificate_key=uuid.uuid4(), email=email)
                else:
                    cer = Certificate.objects.create(certificate_key=uuid.uuid4())
                for component in components:
                    cer.components.add(component)
                return JsonResponse({'certificate_key': cer.certificate_key}, status=status.HTTP_201_CREATED)

        return JsonResponse(data={'msg': 'layout not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=CertificateSerializers,
        description='Удаляет сертификат по ключу сертификата ,если сертификата нет то выдает 404',
        responses={status.HTTP_204_NO_CONTENT: CertificateSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):
        certificate_key = kwargs.get('certificate_key', None)
        obj = get_object_or_404(Certificate, certificate_key = certificate_key)
        obj.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT, data={ 'msg': 'Ok!'})
