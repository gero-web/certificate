from django.http import HttpResponse
from rest_framework.decorators import api_view
from app.helpers.html_to_pdf import to_pdf


@api_view(['get'])
def getPdf(request, certificate_key):
    pdf = to_pdf(certificate_key=certificate_key)
    return pdf
