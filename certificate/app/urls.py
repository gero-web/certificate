from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views.ComponentViews import ComponentViewsSet
from .views.typeComponentViews import TypeComponentViewsSet
from .views.certificateViews import CertificateViewsSet
from .views.layoutViews import LayoutViewsSet
from .views.pdf_view import getPdf
from .views.email_view import email

router = DefaultRouter()
router.register('component', ComponentViewsSet, basename='component')
router.register('type_component', TypeComponentViewsSet, basename='type_component')
router.register('layout', LayoutViewsSet, basename='layout')
router.register('certificate', CertificateViewsSet, basename='certificate')


urlpatterns = [
    path('', include((router.urls, 'app_name'), namespace='api')),
    path('pdf/<slug:certificate_key>/', getPdf, name='get_pdf'),
    path('email/<slug:certificate_key>/', email,
            name='email')
]
