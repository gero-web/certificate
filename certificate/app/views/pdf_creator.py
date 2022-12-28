from io import BytesIO  as StringIO
from weasyprint import HTML
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from reportlab.pdfbase.ttfonts import TTFont
from app.helpers.html_certificate import html_template_certificate
from app.models import Component
from weasyprint import HTML
from django.template.loader import render_to_string

import pdfkit
from easy_pdf.rendering import render_to_pdf_response

import os


def render_to_pdf(req,certificate_key):
   # html = html_template_certificate(certificate_key)
    components = Component.objects.filter(certificate__certificate_key=certificate_key)
    context = {'components': components, 'SITE_URL': settings.SITE_URL }
    html_string = render_to_string('crificate.html', context , request=req) 
   #config=pdfkit.configuration(wkhtmltopdf=r'D:\wkhmtl\wkhtmltopdf\bin\wkhtmltopdf.exe')
  # pdf = pdfkit.from_string(html,False)
    htmldoc = HTML(string=html_string)
    pdf = htmldoc.write_pdf()

    return HttpResponse(pdf, content_type='application/pdf')
     
   
def htmlr(req,certificate_key):
    html = html_template_certificate(certificate_key)   
    return HttpResponse(html)
   # return HttpResponse('We had some errors<pre>%s</pre>' )