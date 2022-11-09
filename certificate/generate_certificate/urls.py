from django.urls import path, include

from .views import Get_Certificate, postExcel

urlpatterns = [
                  path('views/<slug:certificate_key>/', Get_Certificate, name='certificate'),
                  path('views/', postExcel, name='certificate'),
              ]
