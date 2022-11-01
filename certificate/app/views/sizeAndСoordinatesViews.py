from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from app.serializers.invalidSerializers import InvalidSerializer
from rest_framework.viewsets import ModelViewSet
from app.serializers.sizeAndСoordinatesSerializers import SizeAndСoordinatesSerializers
from app.models import SizeAndСoordinates
from drf_spectacular.utils import extend_schema


class SizeAndСoordinatesViewsSet(ModelViewSet):
    queryset = SizeAndСoordinates.objects.all().order_by('pk')
    serializer_class = SizeAndСoordinatesSerializers
    permission_classes = [
        permissions.AllowAny,
    ]

    parser_classes = (
        FormParser,
        MultiPartParser,
    )

    @extend_schema(
        request=SizeAndСoordinatesSerializers,
        responses={status.HTTP_200_OK: SizeAndСoordinatesSerializers, status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super(SizeAndСoordinatesViewsSet, self).list(request, *args, **kwargs)

    @extend_schema(
        request=SizeAndСoordinatesSerializers,
        responses={status.HTTP_200_OK: SizeAndСoordinatesSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super(SizeAndСoordinatesViewsSet, self).update(request, *args, **kwargs)

    @extend_schema(
        request=SizeAndСoordinatesSerializers,
        responses={status.HTTP_200_OK: SizeAndСoordinatesSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super(SizeAndСoordinatesViewsSet, self).retrieve(request, *args, **kwargs)

    @extend_schema(
        request=SizeAndСoordinatesSerializers,
        responses={status.HTTP_200_OK: SizeAndСoordinatesSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=SizeAndСoordinatesSerializers,
        responses={status.HTTP_204_NO_CONTENT: SizeAndСoordinatesSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):
        return super(SizeAndСoordinatesViewsSet, self).destroy(request, *args, **kwargs)


