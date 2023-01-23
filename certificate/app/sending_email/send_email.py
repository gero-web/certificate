from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from app.helpers.html_certificate import html_template_certificate, \
    html_url_certificate
from django.conf import settings


def send(certificate_key, to):
    html = html_template_certificate(certificate_key)
    if html is not None:
        subject = 'Certificate'
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMultiAlternatives(subject,  from_email=from_email, to=to)
        msg.attach_alternative(html, "text/html")
        msg.send()


def send_url(msg,to):
    subject = 'Certificate'
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMessage(subject, msg ,from_email=from_email, to=to)
    msg.content_subtype = 'html'
    msg.send()


def send_pdf(pdf, to, msg = 'Ваш сертификат'):
    subject = 'Certificate'
    from_email = settings.EMAIL_HOST_USER
    msg = EmailMessage(subject, msg ,from_email=from_email, to=to)
    msg.content_subtype = 'html'
    msg.attach('certificate.pdf',pdf ,'application/pdf')
    msg.send()