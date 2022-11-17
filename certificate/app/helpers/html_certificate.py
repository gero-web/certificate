from django.template.loader import get_template
from django.template import Context
from app.models import Certificate,Component
from rest_framework import status


def html_template_certificate(certificate_key):
        components = Component.objects.filter(certificate__certificate_key=certificate_key)
        if not components:
            return None   
        html_template = get_template('crificate.html')
        context = {'components': components}
        html_content = html_template.render(context)
        return html_content