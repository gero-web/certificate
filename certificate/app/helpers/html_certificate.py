from django.template.loader import get_template
from app.models import Component


def html_template_certificate(certificate_key):
    components = Component.objects.filter(certificate__certificate_key=certificate_key)
    if not components:
        return None
    context = {
        'components': components,
    }
    html_content = get_template('crificate.html').render(context)
    return html_content
