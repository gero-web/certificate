import tempfile
from django.http import HttpResponse
from .html_certificate import html_template_certificate
import weasyprint


def to_pdf(certificate_key):
    html = html_template_certificate(certificate_key=certificate_key)
    pdf = weasyprint.HTML(string=html).write_pdf()
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(pdf)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
        return response





