from rest_framework import permissions
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.viewsets import ModelViewSet
from app.serializers.typeComponentSerializers import TypeComponentSerializers
from app.models import TypeComponent
from app.serializers.invalidSerializers import InvalidSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema


class TypeComponentViewsSet(ModelViewSet):
    queryset = TypeComponent.objects.all().order_by('pk')
    serializer_class = TypeComponentSerializers
    permission_classes = [
        permissions.AllowAny,
    ]

    parser_classes = (
        JSONParser,
    )

    @extend_schema(
        request=TypeComponentSerializers,
        responses={status.HTTP_200_OK: TypeComponentSerializers,
                   status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        return super(TypeComponentViewsSet, self).list(request, *args, **kwargs)

    @extend_schema(
        request=TypeComponentSerializers,
        description='Формат входных данных ввидет /type_component/1/ где 1 это  id  type_componet,\n \
            число (обязательный) \n Параметры  передаются ввидет JSON  name: строка  \n',
        responses={status.HTTP_200_OK: TypeComponentSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super(TypeComponentViewsSet, self).update(request, *args, **kwargs)

    @extend_schema(
        request=TypeComponentSerializers,
        description='Формат входных данных ввидет /type_component/1/ где 1 это  id  type_componet, \n  Результат: Возвращает конкретныйtype_componet  \n',
        responses={status.HTTP_200_OK: TypeComponentSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super(TypeComponentViewsSet, self).retrieve(request, *args, **kwargs)

    @extend_schema(
        request=TypeComponentSerializers,
        description='Формат входных данных ввидет /type_component/1/ \
        где 1 это  id  type_componet, \n передаются ввидет JSON  \n паоаметры: name: строка  \n',
        responses={status.HTTP_201_CREATED: TypeComponentSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=TypeComponentSerializers,
        responses={status.HTTP_204_NO_CONTENT: TypeComponentSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):
        return super(TypeComponentViewsSet, self).destroy(request, *args, **kwargs)
