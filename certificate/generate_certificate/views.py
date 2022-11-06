from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import api_view, renderer_classes, \
    parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from app.models import Component
from app.serializers.invalidSerializers import InvalidSerializer
from generate_certificate.serializers.exelserializer import ExcelSerializers
import pandas as pd


@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def Certificate(request, layout_key):
    components = Component.objects.filter(layout__layout_key=layout_key)
    return Response({'components': components}, template_name='crificate.html')


@extend_schema(
    request=ExcelSerializers,
    responses={status.HTTP_200_OK: ExcelSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
)
@api_view(['POST'])
@parser_classes([MultiPartParser])
@renderer_classes([TemplateHTMLRenderer])
def postExcel(request):
    excelSerializer = ExcelSerializers(data=request.data)
    if excelSerializer.is_valid():
        excel = request.data['excel']
        df = pd.read_excel(excel, sheet_name='Sheet1')
        print(df)
    components = Component.objects.filter(layout__layout_key=excelSerializer.data['layout_key'])
    return Response({'components': components}, status=status.HTTP_200_OK,
                    template_name='crificate.html')
