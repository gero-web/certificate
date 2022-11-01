from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from .views.ComponentViews import ComponentViewsSet
from .views.sizeAndСoordinatesViews import SizeAndСoordinatesViewsSet
from .views.typeComponentViews import TypeComponentViewsSet
from .views.attributeViews import AttributeViewsSet
from .views.bodyViews import BodyViewsSet
from .views.certificateViews import CertificateViewsSet
from .views.layoutViews import LayoutViewsSet


router = DefaultRouter()
router.register('component', ComponentViewsSet, basename='component')
router.register('size_and_coordinates', SizeAndСoordinatesViewsSet, basename='size_and_coordinates')
router.register('type_component', TypeComponentViewsSet, basename='type_component')
router.register('attribute', AttributeViewsSet, basename='attribute')
router.register('body', BodyViewsSet, basename='body')
router.register('layout', LayoutViewsSet, basename='layout')
router.register('certificate', CertificateViewsSet, basename='certificate')


urlpatterns = [
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
