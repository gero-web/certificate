from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.viewsets import ModelViewSet
from app.serializers.certificateSerializers import CertificateSerializers
from app.serializers.invalidSerializers import InvalidSerializer
from app.models import Certificate
from drf_spectacular.utils import extend_schema
from rest_framework import status


class CertificateViewsSet(ModelViewSet):

    queryset = Certificate.objects.all().order_by('pk')
    serializer_class = CertificateSerializers
    permission_classes = [
        permissions.AllowAny,
    ]

    parser_classes = (
        FormParser,
        MultiPartParser,
    )

    @extend_schema(
        request=CertificateSerializers,
        responses={status.HTTP_200_OK: CertificateSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super(CertificateViewsSet, self).list(request, *args, **kwargs)

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
        return super(CertificateViewsSet, self).retrieve(request, *args, **kwargs)

    @extend_schema(
        request=CertificateSerializers,
        responses={status.HTTP_200_OK: CertificateSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=CertificateSerializers,
        responses={status.HTTP_204_NO_CONTENT: CertificateSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):

        return super(CertificateViewsSet, self).destroy(request, *args, **kwargs)

