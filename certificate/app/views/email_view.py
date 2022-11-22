from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.decorators import api_view, \
    renderer_classes, \
    parser_classes

from app.models import Certificate
from app.serializers.invalidSerializers import InvalidSerializer
from app.sending_email.send_email import send_url


@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
@extend_schema(
    responses={status.HTTP_200_OK: {'msg': 'sent'}, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    description='У сертификатов у которых не указан email будет сообщение "none email"!'
)
@api_view(['get'])
def email(request, certificate_key):
    question = get_object_or_404(Certificate, certificate_key=certificate_key)
    if question.email == '123@laifr.ru':
        return Response({'msg': 'none email'}, status=status.HTTP_200_OK)
    send_url(question.certificate_key, [question.email])
    return Response({'msg': 'sent'}, status=status.HTTP_200_OK)
