from django.http import FileResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view, \
    renderer_classes, \
    parser_classes
from rest_framework import status
from app.serializers.invalidSerializers import InvalidSerializer
from drf_spectacular.utils import extend_schema
from app.models import PdfCertificate
from img2pdf import convert, mm_to_pt, get_layout_fun
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http.response import JsonResponse
from app.serializers.pdfGeneratorImageSerializers import PdfGeneratorImageSerializers,PdfGetCertificate, \
PdfEmailKeysSerializers, PdfOne_img_one_pdf
from app.sending_email.send_email import send_url
from app.helpers.html_certificate import html_url_certificate
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
import base64,io

def render_pdf(img,orientation):
      
        if orientation == 'vertical':
            letter = (mm_to_pt(210), mm_to_pt(297)) # A4
        else:
            letter = (mm_to_pt(420), mm_to_pt(297)) # A3
        layout = get_layout_fun(letter)
        file = base64.b64decode(img.split('base64,')[1])
        file = io.BytesIO(file)   
        pdf = convert(file, layout_fun = layout)
        return pdf
       


@extend_schema(
    request = PdfEmailKeysSerializers,
    responses={status.HTTP_200_OK: {'msg': 'sent'}, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    description='отправляет сылку которая должна вести на фронт"!'
)
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
def render_to_pdf_email(req):
    req_file =  PdfEmailKeysSerializers(data=req.data)
    if req_file.is_valid(): 
        lst_exp = []
        for key in req_file.data['keys']:
            pdf_cert = PdfCertificate.objects.filter(key=key).first()
            if pdf_cert:
                print(key)
                msg = html_url_certificate(pdf_cert.key)
                to = (pdf_cert.email,) #, 'annivino@mail.ru'
                send_url( msg, to)
            else:
                lst_exp.append(key) 
        response = JsonResponse(data= {'msg':'ok', 'error_key': lst_exp}, status=status.HTTP_200_OK)
        return response
    else:
         return HttpResponse('body empty', status= status.HTTP_400_BAD_REQUEST)
   

@extend_schema(
    request = PdfGetCertificate,
    responses={status.HTTP_200_OK: {'msg': 'sent'}, status.HTTP_404_NOT_FOUND: InvalidSerializer},
    description='Отдает сертификат виде pdf "!'
)
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
def get_pdf(req):
    req_file =  PdfGetCertificate(data=req.data )
    if req_file.is_valid(): 
        pdf_cert = get_object_or_404(PdfCertificate, key=req_file.data['key'])
        
        b64 = base64.b64encode(pdf_cert.path.read())
        encoded_str = b64.decode('utf-8')
        return JsonResponse({ 'pdf': "data:application/pdf;base64,"+ encoded_str}, status = status.HTTP_200_OK)
    else:
         return HttpResponse('body empty', status= status.HTTP_400_BAD_REQUEST)    

@extend_schema(
    request = PdfGeneratorImageSerializers,
    responses={status.HTTP_200_OK: {'msg': 'sent'}, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    description='Создает 1 pdf из картинки "!'
)
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
def render_to_pdf(req):
    req_file =  PdfGeneratorImageSerializers(data=req.data, many= True )
    if req_file.is_valid(): 
        for  data in req_file.data:
            pdf = render_pdf(data['image'], orientation = data['orientation'])
            p =  PdfCertificate.objects.create( email = data['email'], key = data['key'], orientation =  data['orientation'])
            p.path = ContentFile(pdf, name=data['key'] + '.pdf')
            p.save()  
        return JsonResponse(data= {'msg':'ok'}, status=status.HTTP_200_OK)
    else:
         return HttpResponse('body empty', status= status.HTTP_400_BAD_REQUEST)       
     
     
     
@extend_schema(
    request = PdfOne_img_one_pdf,
    responses={status.HTTP_200_OK: {'msg': 'sent'}, status.HTTP_400_BAD_REQUEST: InvalidSerializer},
    description='Создает 1 pdf из картинки "!'
)
@api_view(['POST'])
@renderer_classes([JSONRenderer])
@parser_classes([JSONParser])
def one_image_one_pdf(req):
    req_file =  PdfOne_img_one_pdf(data=req.data)
    if req_file.is_valid(): 
        pdf = render_pdf(req_file.data['image'], orientation =  req_file.data['orientation'])
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=certificate'          
        return response
    else:
         return HttpResponse('body empty', status= status.HTTP_400_BAD_REQUEST)       