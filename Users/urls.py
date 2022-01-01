from django.urls import path
from Users import views as user_views

urlpatterns = [
    path('', user_views.users, name='users'),
    path('delete/<str:username>', user_views.delete_user),
    path('disable/<str:username>/<disabled_status>', user_views.disable_user),
    path('create-new/', user_views.create_new_user, name='create_new_user'),
]