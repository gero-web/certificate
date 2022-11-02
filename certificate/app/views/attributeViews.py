from rest_framework import permissions
from rest_framework.parsers import JSONParser, FormParser
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from app.serializers.attributeSerializers import AttributeSerializers
from app.serializers.invalidSerializers import InvalidSerializer
from app.models import Attribute
from drf_spectacular.utils import extend_schema


class AttributeViewsSet(ModelViewSet):
    queryset = Attribute.objects.all().order_by('pk')
    serializer_class = AttributeSerializers
    permission_classes = [
        permissions.AllowAny,
    ]

    parser_classes = (
        FormParser,
        JSONParser,
    )

    @extend_schema(
        request=AttributeSerializers,
        responses={status.HTTP_200_OK: AttributeSerializers, status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super(AttributeViewsSet, self).list(request, *args, **kwargs)

    @extend_schema(
        request=AttributeSerializers,
        responses={status.HTTP_200_OK: AttributeSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super(AttributeViewsSet, self).update(request, *args, **kwargs)

    @extend_schema(
        request=AttributeSerializers,
        responses={status.HTTP_200_OK: AttributeSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super(AttributeViewsSet, self).retrieve(request, *args, **kwargs)

    @extend_schema(
        request=AttributeSerializers,
        responses={status.HTTP_200_OK: AttributeSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super(AttributeViewsSet, self).create(request, *args, **kwargs)

    @extend_schema(
        request=AttributeSerializers,
        responses={status.HTTP_204_NO_CONTENT: AttributeSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):
        return super(AttributeViewsSet, self).destroy(request, *args, **kwargs)
