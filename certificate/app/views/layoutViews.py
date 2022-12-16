import uuid
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from app.serializers.layoutSerializer import LayoutSerializer
from app.serializers.invalidSerializers import InvalidSerializer
from app.serializers.componentSerializers import ComponentSerializers
from app.models import Layout
from app.models import Component
from app.models import TypeComponent
from drf_spectacular.utils import extend_schema
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from app.helpers.delete_cache import del_cache


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

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*6,key_prefix='layout_key'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
        
    @extend_schema(
        request=LayoutSerializer,
        description='выводи все ключи layout',
        responses={status.HTTP_200_OK: LayoutSerializer,  status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        queryset = Layout.objects.all().values_list('layout_key').distinct('layout_key')
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(page)
      
        return Response(page)

    @extend_schema(
        request=LayoutSerializer,
        description='При обновление  layout , создаются component  если не указан id и сылется на него, елсли id указан то обновляет компонет \n \
             должен быть создан зарание \n id  идентификатор компонента тип данных число ',
        responses={status.HTTP_200_OK: LayoutSerializer, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        layout_key = kwargs.get('layout_key', None)
        layout = Layout.objects.filter(layout_key = layout_key).exists()
        if not layout:
            return Response(data={'msg': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer: LayoutSerializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid(raise_exception=True)
        if is_valid:
            components = request.data['component']
            if not components:
                return Response(data={'msg': 'Components empty'}, status=status.HTTP_400_BAD_REQUEST)
            allSerializesComponents = [(component.get('id',None), ComponentSerializers(data=component)) for component in components]
            is_allValidComponent = all([comp[1].is_valid() for comp in allSerializesComponents])
            if is_allValidComponent:
               
                for id,comp in allSerializesComponents:
                      if id:
                          obj = get_object_or_404( Component, pk = id)
                          if obj:
                            comp.update(obj, comp.validated_data)
                      else:
                            obj = comp.save()
                            Layout.objects.create(component=obj, layout_key=layout_key)
            else:
                return Response(data={'msg': 'Component is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        del_cache('layout_key')
        return Response(data={'layout_key': layout_key}, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=LayoutSerializer,
        description='При получение  layout необходимо передать layout_key,\n возвращает список component связанных с этим layout ',
        responses={status.HTTP_200_OK: LayoutSerializer, status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        key = kwargs.get('layout_key', None)
        queryset = Component.objects.filter(layout__layout_key=key).select_related()

        if not queryset:
            return Response('layout key not found', status=status.HTTP_404_NOT_FOUND)

        serializer = ComponentSerializers(data=queryset, many=True, context={"request": request})
        serializer.is_valid()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @extend_schema(
        request=LayoutSerializer,
         description='При создание  layout , создаются components формат json  и является списком который содержит component - ы  \n \
             поле image  работает с двумя типами данных \n 1. base64 \n 2. url картинки \n  type -- это id type_componet , type_comonent \n \
             должен быть создан зарание',
        responses={status.HTTP_201_CREATED: LayoutSerializer, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        type = TypeComponent.objects.all()
        if not type:
            TypeComponent.objects.create(name='image')
            TypeComponent.objects.create(name='background')
            TypeComponent.objects.create(name='text')
            TypeComponent.objects.create(name='mainBackground')

        serializer: LayoutSerializer = self.get_serializer(data=request.data)
        is_valid = serializer.is_valid(raise_exception=True)
        if is_valid:
            components = request.data['component']
            if not components:
                return Response(data={'msg': 'Components empty'}, status=status.HTTP_400_BAD_REQUEST)
            allSerializesComponents = [ComponentSerializers(data=component) for component in components]
            is_allValidComponent = all([comp.is_valid() for comp in allSerializesComponents])
            if is_allValidComponent:
                saved_component = [comp.save() for comp in allSerializesComponents]
                layout_key = uuid.uuid4()
                for comp in saved_component:
                    Layout.objects.create(component=comp, layout_key=layout_key)
            else:
                return Response(data={'msg': 'Component is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        del_cache('layout_key')
        return Response(data={'layout_key': layout_key}, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=LayoutSerializer,
        description='При удаление  layout  удалеются все компонеты свзязанные с этим layout и \n  \
            certificate',
        responses={status.HTTP_204_NO_CONTENT: LayoutSerializer, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):
        key = kwargs.get('layout_key', None)
        queryset = Component.objects.filter(layout__layout_key=key).select_related()

        if not queryset:
            return Response('layout key not found', status=status.HTTP_404_NOT_FOUND)
        cetificate = queryset[0].certificate_set.all()
        cetificate.delete()
        queryset.delete()
        del_cache('layout_key')
        return Response(status=status.HTTP_204_NO_CONTENT)
