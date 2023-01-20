from django.http import FileResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view, \
    renderer_classes, \
    parser_classes
from rest_framework import status
from app.serializers.invalidSerializers import InvalidSerializer
from drf_spectacular.utils import extend_schema
from app.helpers.html_certificate import html_template_certificate
from img2pdf import convert, mm_to_pt, get_layout_fun
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from app.serializers.pdfGeneratorImageSerializers import PdfGeneratorImageSerializers
from app.sending_email.send_email import send_pdf
import base64,io



@extend_schema(
    request = PdfGeneratorImageSerializers,
    responses={status.HTTP_200_OK: {'msg': 'sent'}, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    description='Создает 1 pdf из картинки "!'
)
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
def render_to_pdf(req):
    req_file =  PdfGeneratorImageSerializers(data=req.data)
    if req_file.is_valid(): 
        letter = (mm_to_pt(210), mm_to_pt(297)) # A4
        # letter = (mm_to_pt(420), mm_to_pt(297)) # A3
        layout = get_layout_fun(letter)
        lst_img = []
        for data in  req_file.data['image']:
            file = base64.b64decode(data.split('base64,')[1])
            file = io.BytesIO(file)  
            lst_img.append(file)
      
        pdf = convert(lst_img, layout_fun = layout)
        to = ['sergeq198@gmail.com']
        send_pdf(pdf, to )
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=certificate'  
        return response
    else:
         return HttpResponse('body empty', status= status.HTTP_400_BAD_REQUEST)
   
      
       