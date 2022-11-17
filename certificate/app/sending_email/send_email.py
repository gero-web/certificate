from django.core.mail import send_mail
from app.helpers.html_certificate import html_template_certificate
from  django.conf import settings

def send(certificate_key, to):
    html  = html_template_certificate(certificate_key)
    if html  is  not None:
        subject = 'Certificate'
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, 'Test', from_email, to, html_message=html)