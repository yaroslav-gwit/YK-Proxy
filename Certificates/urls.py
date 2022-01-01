from django.urls import path
from Certificates import views as certificates_views

urlpatterns = [
    path('', certificates_views.certificates, name='certificates'),
]