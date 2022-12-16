from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings

def html_url_certificate(certificate_key):

    context = {'certificate_key': certificate_key,
               'domain': settings.SITE_URL, }
    html_content = get_template('url.html').render(context)
    return html_content

def send_url(certificate_key, to):
    html = html_url_certificate(certificate_key)
    if html is not None:
       subject = 'Certificate'
       from_email = settings.EMAIL_HOST_USER
       msg = EmailMultiAlternatives(subject, from_email=from_email, to=to)
       msg.attach_alternative(html, "text/html")
       msg.send()
