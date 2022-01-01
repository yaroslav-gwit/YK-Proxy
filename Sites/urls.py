from django.urls import path
from Sites import views as site_views

urlpatterns = [
    path('', site_views.sites, name='sites'),
    path('create-new-site/', site_views.create_new_site, name='create_new_site'),
    path('haproxy-generate-template/', site_views.haproxy_generate_template, name='haproxy_generate_template'),
    path('delete/<int:site_id>', site_views.delete_site),
    path('disable/<int:site_id>/<disabled_status>', site_views.disable_site),
    path('maintenance/<int:site_id>/<maintenance_status>', site_views.maintenance_site),
]