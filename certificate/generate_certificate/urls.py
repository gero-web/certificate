from django.urls import path, include

from .views import Certificate, postExcel

urlpatterns = [
                  path('views/<slug:layout_key>/', Certificate, name='certificate'),
                  path('views/', postExcel, name='certificate'),
              ]
