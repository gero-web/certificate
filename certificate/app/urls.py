from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views.ComponentViews import ComponentViewsSet
from .views.typeComponentViews import TypeComponentViewsSet
from .views.certificateViews import CertificateViewsSet
from .views.layoutViews import LayoutViewsSet
from .views.email_view import email

from app.views.pdf_creator import render_to_pdf, get_pdf,render_to_pdf_email, \
    one_image_one_pdf


router = DefaultRouter()
router.register('component', ComponentViewsSet, basename='component')
router.register('type_component', TypeComponentViewsSet, basename='type_component')
router.register('layout', LayoutViewsSet, basename='layout')
router.register('certificate', CertificateViewsSet, basename='certificate')


urlpatterns = [
    path('', include((router.urls, 'app_name'), namespace='api')),
    path('save_pdf/', render_to_pdf, name='save_pdf' ),
    path('get_pdf/', get_pdf, name='get_pdf' ),
     path('one_image_one_pdf/', one_image_one_pdf, name='one_image_one_pdf' ),
    path('pdf_sendEmail/', render_to_pdf_email, name='pdf_sendEmail' ),
    path('email/<slug:certificate_key>/', email,name='email'),
]
