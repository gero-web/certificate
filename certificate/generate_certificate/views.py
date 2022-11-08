import uuid
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import api_view, renderer_classes, \
    parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.http.response import JsonResponse
from app.models import Component, Certificate, Layout
from app.serializers.invalidSerializers import InvalidSerializer
from generate_certificate.serializers.exelserializer import ExcelSerializers
import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile;


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def Get_Certificate(request, certificate_key):
    components = Component.objects.filter(certificate__certificate_key=certificate_key)
    if not components:
        return JsonResponse(data={'msg': 'certificate not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'components': components}, template_name='crificate.html')


@extend_schema(
    request=ExcelSerializers,
    responses={status.HTTP_200_OK: ExcelSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
)
@api_view(['POST'])
@parser_classes([MultiPartParser])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def postExcel(request):
    excelSerializer = ExcelSerializers(data=request.data)
    if excelSerializer.is_valid():
        components = Component.objects.filter(layout__layout_key=excelSerializer.data['layout_key'])
        cer = Certificate.objects.create(certificate_key=uuid.uuid4())
        for component in components:
            cer.components.add(component)
            print(cer)

    components = Component.objects.filter(layout__layout_key=excelSerializer.data['layout_key'])
    if not components:
        return JsonResponse(data={'msg': 'layout not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'components': components}, status=status.HTTP_200_OK,
                    template_name='crificate.html')


def excel():
    excelSerializer = ExcelSerializers(data=request.data)
    if excelSerializer.is_valid():
        # excel only
        excel: InMemoryUploadedFile = request.data['excel']
        typeFile = excel.name[excel.name.rindex('.') + 1:]
        df = pd.read_excel(excel)
        lst = list(zip(*([*i.values()] for i in df.to_dict().values())))
        print(df.to_dict())
        print(lst)
