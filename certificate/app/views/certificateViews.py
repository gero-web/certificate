from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.viewsets import ModelViewSet
from app.serializers.certificateSerializers import CertificateSerializers
from app.serializers.tagSerializers import TagSerializer
from app.serializers.exelserializer import ExcelSerializers
from app.serializers.invalidSerializers import InvalidSerializer
from app.models import Certificate, Component
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from app.helpers.html_certificate import html_template_certificate
from app.serializers.componentSerializers import ComponentSerializers
import uuid


class CertificateViewsSet(ModelViewSet):
    queryset = Certificate.objects.all().order_by('pk')
    serializer_class = CertificateSerializers
    permission_classes = [
        permissions.AllowAny,
    ]
    lookup_field = 'certificate_key'

    parser_classes = (
        MultiPartParser,
        JSONParser,

    )

    renderer_classes = (

        JSONRenderer,
        TemplateHTMLRenderer,
    )

    @extend_schema(
        description='Возвращает список сертификатов!',
        responses={status.HTTP_200_OK: {'certificates': f'pk: {uuid.uuid4}'},
                  status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def list(self, request, *args, **kwargs):
        queryset = Certificate.objects.all().order_by('certificate_key').values_list('certificate_key')\
        .distinct('certificate_key')
        queryset = self.filter_queryset(queryset)
      
        page = self.paginate_queryset(queryset)
       
        if page is not None:
             return JsonResponse(data={'certificates': page})
       
        return JsonResponse(data={'certificates': page})

    @extend_schema(
        request=CertificateSerializers,
        description='Не реализован и не должен проверятся на данный момент!',
        responses={status.HTTP_200_OK: CertificateSerializers, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def update(self, request, *args, **kwargs):
        return super(CertificateViewsSet, self).update(request, *args, **kwargs)
    
    
    @extend_schema(
        request=TagSerializer,
        description='Не реализован и не должен проверятся на данный момент!',
        responses={status.HTTP_200_OK: CertificateSerializers , status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    @action(detail=False, methods=['POST'], 
            url_path='get_all_certificate',
            url_name='get_all_certificate')
    
    def get_all_certificate(self, req):
       tag = TagSerializer(data=req.data)
       tag.is_valid()
       data = []
       if(tag.is_valid()):
           keys = tag.data.get('certificate_keys')
           for key in keys:
               queryset = Component.objects.filter(certificate__certificate_key=key).select_related()
               if not queryset:
                   return Response('certificate key not found', status=status.HTTP_404_NOT_FOUND)
               serializer = ComponentSerializers(data=queryset, many=True, context={"request": req})
               serializer.is_valid()
               data.append(serializer.data)

           return Response(data, status=status.HTTP_200_OK)
       return Response('certificate key not found', status=status.HTTP_404_NOT_FOUND)
    
    # def get_all_certificate(self,req):
    #     tag = TagSerializer(data = req.data)
    #     tag.is_valid()
    #     if( tag.is_valid()):
    #         keys = [Certificate.objects.filter(certificate_key = key['certificate_key']).first() for key in tag.data['certificate_keys']]
    #         if(all(keys)):
    #             certificates = CertificateSerializers(data=keys, many=True)
    #             certificates.is_valid()
    #             return Response(certificates.data,  status=status.HTTP_200_OK)
            
    #     return Response({'msg': 'один или несколько certificate_key не найден'},  status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
        # request=CertificateSerializers,
        description='Возвращает конкретный сертификат виде html страницы, если сертификат не найдет вернет JSON',
        responses={status.HTTP_200_OK: {},
                   status.HTTP_500_INTERNAL_SERVER_ERROR: InvalidSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        certificate_key = kwargs['certificate_key']
        queryset = Component.objects.filter(certificate__certificate_key=certificate_key).select_related()
        if not queryset:
            return Response('certificate key not found', status=status.HTTP_404_NOT_FOUND)
        serializer = ComponentSerializers(data=queryset, many=True, context={"request": request})
        serializer.is_valid()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


    @extend_schema(
        request=ExcelSerializers,
        description='Создает сертификат email необязательное',
        responses={status.HTTP_201_CREATED: uuid.uuid4(), status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    )
    def create(self, request, *args, **kwargs):
        k = []
        exelSerializer = ExcelSerializers(data=request.data)
        print(exelSerializer.is_valid())
        print(exelSerializer.data)
        if exelSerializer.is_valid():
            components = Component.objects.filter(layout__layout_key=exelSerializer.data['layout_key'])
           
            exel = exelSerializer.data['exel']
            if components:
                if exel:
                    for e in range(len(exel)):
                        if exel[e].get("email"):
                            cer = Certificate.objects.create(certificate_key=uuid.uuid4(), email=exel[e].get("email"))
                        else:
                            cer = Certificate.objects.create(certificate_key=uuid.uuid4())
                        k.append(cer.certificate_key)
                        for component in components:
                            if component.anchor_number:
                                new_component = component
                                new_component.text = exel[e].get(component.anchor_number)
                                new_comp = Component.objects.create(type=new_component.type, color=new_component.color,
                                                                    font=new_component.font,
                                                                    font_size=new_component.font_size,
                                                                    font_weight=new_component.font_weight,
                                                                    x=new_component.x, y=new_component.y,
                                                                    width=new_component.width,
                                                                    height=new_component.height,
                                                                    text=new_component.text,
                                                                    image=new_component.image,
                                                                    opacity=new_component.opacity,
                                                                    text_align=new_component.text_align,
                                                                    font_style=new_component.font_style,
                                                                    text_decoration=new_component.text_decoration,
                                                                    anchor_number=new_component.anchor_number)
                                cer.components.add(new_comp)
                            else:
                                cer.components.add(component)
                return JsonResponse({'certificate_key': k}, status=status.HTTP_201_CREATED)

        return JsonResponse(data={'msg': 'layout not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=CertificateSerializers,
        description='Удаляет сертификат по ключу сертификата ,если сертификата нет то выдает 404',
        responses={status.HTTP_204_NO_CONTENT: CertificateSerializers, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    )
    def destroy(self, request, *args, **kwargs):
        certificate_key = kwargs.get('certificate_key', None)
        obj = get_object_or_404(Certificate, certificate_key=certificate_key)
        obj.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT, data={ 'msg': 'Ok!'})
