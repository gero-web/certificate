import json
import uuid
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app.serializers.layoutSerializer import LayoutSerializer
from app.serializers.invalidSerializers import InvalidSerializer
from app.serializers.componentSerializers import ComponentSerializers
from app.models import Layout
from app.models import Component
from drf_spectacular.utils import extend_schema
from rest_framework import status


class LayoutViewsSet(ModelViewSet):
    queryset = Layout.objects.all().order_by('pk')
    serializer_class = LayoutSerializer
    permission_classes = [
        permissions.AllowAny,
    ]
    lookup_field = 'layout_key'

    parser_classes = (
        JSONParser,
        MultiPartParser,
    )

    @extend_schema(
        request=LayoutSerializer,
        responses={status.HTTP_200_OK: LayoutSerializer, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        queryset = Layout.objects.all().values_list('pk', 'layout_key')
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            #  serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(json.dumps(page))
        # serializer = self.get_serializer(filter, many=True)
        return Response(json.dumps(page))

    @extend_schema(
        request=LayoutSerializer,
        responses={status.HTTP_200_OK: LayoutSerializer, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super(LayoutViewsSet, self).update(request, *args, **kwargs)

    @extend_schema(
        request=LayoutSerializer,
        responses={status.HTTP_200_OK: LayoutSerializer, status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        key = kwargs.get('layout_key', None)
        queryset = Component.objects.filter(layout__layout_key=key).select_related()

        if not queryset:
            return Response(json.dumps('layout key not found'), status=status.HTTP_404_NOT_FOUND)

        serializer = ComponentSerializers(data=queryset, many=True, context={"request": request})
        serializer.is_valid()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @extend_schema(
        request=LayoutSerializer,
        responses={status.HTTP_201_CREATED: LayoutSerializer, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer: LayoutSerializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid(raise_exception=True)
        if is_valid:
            components = request.data['component']
            if not components:
                 return Response(data={'msg': 'Components empty'}, status=status.HTTP_400_BAD_REQUEST)
            allSerializesComponents = [ComponentSerializers(data=component) for component in components]
            is_allValidComponent = all([comp.is_valid() for comp in allSerializesComponents])
            print(is_allValidComponent)
            if is_allValidComponent:
                saved_component = [comp.save() for comp in allSerializesComponents]
                layout_key = uuid.uuid4()
                for comp in saved_component:
                    Layout.objects.create(component=comp, layout_key=layout_key)
            else:
                return Response(data={'msg': 'Component is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        else:
    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
        return Response(data={'layout_key':layout_key}, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=LayoutSerializer,
        responses={status.HTTP_204_NO_CONTENT: LayoutSerializer, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):
        key = kwargs.get('layout_key', None)
        queryset = Component.objects.filter(layout__layout_key=key).select_related()

        if not queryset:
            return Response(json.dumps('layout key not found'), status=status.HTTP_404_NOT_FOUND)

        for comp in queryset:
            comp.delete()
        return Response( status=status.HTTP_200_OK)
