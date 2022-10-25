from cgitb import reset
from turtle import width
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ComponentSeralizers, LayoutSerializers, HtmlSerializers, AttributeSerializers
from .models import Layout


class ComponentViewsSet(ModelViewSet):

    queryset = Layout.objects.all()
    serializer_class = LayoutSerializers
    permission_classes = [
        permissions.AllowAny,
    ]
    
    parser_classes = (
                        FormParser, 
                        MultiPartParser, 
                    )
    
    @staticmethod
    def _parse_req(request)-> tuple:
        '''
            return tuple(data_html, data_component, data_attribute)
        '''
        data_html = {
           'text': request.data.get('text',   None),
           'name': request.data.get('name',   None),
           'image': request.data.get('image', None),
         }
        
        data_component = {
             'type': request.data.get('type', None),
             'x': request.data.get('x', None),
             'z': request.data.get('z', None),
             'y': request.data.get('y', None),
             'width': request.data.get('width', None),
             'height': request.data.get('height', None),     
        }
   
        
        data_attribute = {
             'color': request.data.get('color',None),
             'font': request.data.get('font',None),
             'font_size': request.data.get('font_size',None),
             'font_weight': request.data.get('font_weight',None),
        }
        
        return  data_html,data_component, data_attribute 
    
    def create(self, request, *args, **kwargs):
        data_html,data_component, data_attribute = self._parse_req(request)
        attribute = AttributeSerializers(data=data_attribute)
        html = HtmlSerializers(data=data_html)
        component = ComponentSeralizers(data=data_component)
        
        if html.is_valid() and component.is_valid() and attribute.is_valid():
           h =  html.save()    
           attr = attribute.save()
           comp = component.save()
           Layout.objects.create(html=h,component=comp, attribute=attr)
          
           return Response(status=HTTP_201_CREATED)
       
        return Response(status=HTTP_400_BAD_REQUEST)
    
    
  
        