from io import BytesIO, StringIO
from django.http import HttpResponse
from django.conf import settings
from .html_certificate import html_template_certificate
from xhtml2pdf import pisa

import os


def to_pdf(certificate_key):
    html = html_template_certificate(certificate_key=certificate_key)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), result,  encoding='UTF-8',
                            link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type ='application/pdf')
    return None


def fetch_resources(uri, rel):
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))

    else:
        path = None
    return path

