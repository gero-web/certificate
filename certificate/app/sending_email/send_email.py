from django.core.mail import EmailMultiAlternatives
from app.helpers.html_certificate import html_template_certificate
from django.conf import settings


def send(certificate_key, to):
    html = html_template_certificate(certificate_key)
    if html is not None:
        subject = 'Certificate'
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(subject,  from_email=from_email, to=to)
        msg.attach_alternative(html, "text/html")
        msg.send()
