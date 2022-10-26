from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from app.serializers.layoutSerializers import LayoutSerializers
from app.models import Layout
from drf_spectacular.utils import extend_schema


class LayoutViewsSet(ModelViewSet):
    queryset = Layout.objects.all()
    serializer_class = LayoutSerializers
    permission_classes = [
        permissions.AllowAny,
    ]

    parser_classes = (
        FormParser,
        MultiPartParser,
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        request=LayoutSerializers,
        responses={201: LayoutSerializers},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
