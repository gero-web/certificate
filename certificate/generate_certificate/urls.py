from django.urls import path, include

from .views import CertificateView


urlpatterns = [
                  path('views/<slug:layout_key>/', CertificateView.as_view()),

              ]
