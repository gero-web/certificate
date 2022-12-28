from django.http import FileResponse
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from app.helpers.html_certificate import html_template_certificate
from app.models import Component
from weasyprint import HTML
from django.template.loader import render_to_string



import os


def render_to_pdf(req,certificate_key):
    components = Component.objects.filter(certificate__certificate_key=certificate_key)
    context = {'components': components, 'SITE_URL': settings.SITE_URL }
    html_string = render_to_string('crificate.html', context , request=req) 
    htmldoc = HTML(string=html_string)
    pdf = htmldoc.write_pdf()

    return HttpResponse(pdf, content_type='application/pdf')
     
   
def htmlr(req,certificate_key):
    html = html_template_certificate(certificate_key)   
    return HttpResponse(html)
   # return HttpResponse('We had some errors<pre>%s</pre>' )