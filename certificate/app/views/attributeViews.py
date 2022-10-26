from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app.serializers.attributeSerializers import AttributeSerializers
from app.models import Attribute
from drf_spectacular.utils import extend_schema


class AttributeViewsSet(ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializers
    permission_classes = [
        permissions.AllowAny,
    ]

    parser_classes = (
        FormParser,
        MultiPartParser,
    )

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Attribute.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = AttributeSerializers(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})
