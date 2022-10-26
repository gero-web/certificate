from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from .views.layoutViews import LayoutViewsSet
from .views.componentViews import ComponentViewsSet
from .views.typeComponentViews import TypeComponentViewsSet
from .views.attributeViews import AttributeViewsSet
from .views.htmlViews import HtmlViewsSet


router = DefaultRouter()
router.register('layout', LayoutViewsSet, basename='layout')
router.register('component', ComponentViewsSet, basename='component')
router.register('component/<int:pk>/', ComponentViewsSet, basename='component')
router.register('type_component', TypeComponentViewsSet, basename='type_component')
router.register('type_component/<int:pk>/', TypeComponentViewsSet, basename='type_component')
router.register('attribute', AttributeViewsSet, basename='attribute')
router.register('attribute/<int:pk>/', AttributeViewsSet, basename='attribute')
router.register('html', HtmlViewsSet, basename='html')
router.register('html/<int:pk>/', HtmlViewsSet, basename='html')

urlpatterns = [
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
