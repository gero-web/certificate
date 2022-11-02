from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework import status
from app.serializers.invalidSerializers import InvalidSerializer
from rest_framework.viewsets import ModelViewSet
from app.serializers.bodySerializers import BodySerializers
from app.models import Body
from drf_spectacular.utils import extend_schema


class BodyViewsSet(ModelViewSet):
    queryset = Body.objects.all().order_by('pk')
    serializer_class = BodySerializers
    permission_classes = [
        permissions.AllowAny,
    ]

    parser_classes = (
        FormParser,
        MultiPartParser,
        JSONParser,
    )

    @extend_schema(
        request=BodySerializers,
        responses={status.HTTP_200_OK: BodySerializers, status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super(BodyViewsSet, self).list(request, *args, **kwargs)

    @extend_schema(
        request=BodySerializers,
        responses={status.HTTP_200_OK: BodySerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super(BodyViewsSet, self).update(request, *args, **kwargs)

    @extend_schema(
        request=BodySerializers,
        responses={status.HTTP_200_OK: BodySerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super(BodyViewsSet, self).retrieve(request, *args, **kwargs)

    @extend_schema(
        request=BodySerializers,
        responses={status.HTTP_200_OK: BodySerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super(BodyViewsSet, self).create(request, *args, **kwargs)

    @extend_schema(
        request=BodySerializers,
        responses={status.HTTP_204_NO_CONTENT: BodySerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):
        return super(BodyViewsSet, self).destroy(request, *args, **kwargs)