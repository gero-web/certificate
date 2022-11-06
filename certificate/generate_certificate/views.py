from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Component


class CertificateView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'crificate.html'

    def get(self, request, layout_key):
        components = Component.objects.filter(layout__layout_key=layout_key)

        return Response({'components':components})
from django.shortcuts import render

# Create your views here.
