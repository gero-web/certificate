from django.urls import path,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from .views import ComponentViewsSet

router = DefaultRouter()
router.register('component', ComponentViewsSet, basename='component')

urlpatterns = [
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
