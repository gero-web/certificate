from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.viewsets import ModelViewSet
from app.serializers.componentSerializers import ComponentSerializers
from app.serializers.invalidSerializers import InvalidSerializer
from app.models import Component
from drf_spectacular.utils import extend_schema
from rest_framework import status


class ComponentViewsSet(ModelViewSet):

    queryset = Component.objects.all().order_by('pk')
    serializer_class = ComponentSerializers
    permission_classes = [
        permissions.AllowAny,
    ]

    parser_classes = (
        FormParser,
        MultiPartParser,
        JSONParser,
    )

    @extend_schema(
        request=ComponentSerializers,
        responses={status.HTTP_200_OK: ComponentSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super(ComponentViewsSet, self).list(request, *args, **kwargs)

    @extend_schema(
        request=ComponentSerializers,
        responses={status.HTTP_200_OK: ComponentSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super(ComponentViewsSet, self).update(request, *args, **kwargs)

    @extend_schema(
        request=ComponentSerializers,
        responses={status.HTTP_200_OK: ComponentSerializers, status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super(ComponentViewsSet, self).retrieve(request, *args, **kwargs)

    @extend_schema(
        request=ComponentSerializers,
        responses={status.HTTP_200_OK: ComponentSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        print(request)
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=ComponentSerializers,
        responses={status.HTTP_204_NO_CONTENT: ComponentSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):

        return super(ComponentViewsSet, self).destroy(request, *args, **kwargs)

