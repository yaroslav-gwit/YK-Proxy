from django.urls import path
from Dashboard import views as dashboard_views

urlpatterns = [
    path('', dashboard_views.dashboard, name='dashboard'),
]