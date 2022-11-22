from django.conf import settings
from django.template.loader import get_template
from app.models import Component


def html_template_certificate(certificate_key):
    components = Component.objects.filter(certificate__certificate_key=certificate_key)
    if not components:
        return None
    context = {'components': components, }
    html_content = get_template('crificate.html').render(context)
    return html_content


def html_url_certificate(certificate_key):

    context = {'certificate_key': certificate_key,
               'domain': settings.SITE_URL, }
    html_content = get_template('url.html').render(context)
    return html_content
