import tempfile
from django.http import HttpResponse
from .html_certificate import html_template_certificate
from django.conf import settings
import pdfkit


def to_pdf(certificate_key):
    options = {
        'encoding': "UTF-8",
    }
    css =  settings.STATICFILES_DIRS[0] + '/styles/style.css'
    html = html_template_certificate(certificate_key=certificate_key)
    pdf = pdfkit.PDFKit(html, 'string', css=css, options=options, verbose=True)
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=False) as output:
        output.write(pdf.to_pdf())
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
        return response





